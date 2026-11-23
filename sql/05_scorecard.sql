-- Launch scorecard: each success criterion from the program brief, overall and by channel
-- The blended number can pass while one channel fails, so both are shown
WITH acct AS (
    SELECT a.channel, a.account_id, MAX(o.order_id) IS NOT NULL AS bought
    FROM accounts a
    LEFT JOIN orders o USING (account_id)
    WHERE a.plan IN ('Team', 'Business', 'Enterprise')
    GROUP BY a.channel, a.account_id
),
attach AS (
    SELECT COALESCE(channel, 'overall') AS channel, 100.0 * AVG(bought::INT) AS v
    FROM acct GROUP BY ROLLUP (channel)
),
ord AS (
    SELECT
        COALESCE(channel, 'overall')                                            AS channel,
        100.0 * AVG(activated_14d::INT)                                         AS activation,
        100.0 * AVG(CASE WHEN days_to_access <= 1 THEN 1 ELSE 0 END)            AS within_24h,
        100.0 * AVG(CASE WHEN ABS(billed_amount - expected_amount) > 0.005 * expected_amount THEN 1 ELSE 0 END) AS billing_error
    FROM orders GROUP BY ROLLUP (channel)
),
long AS (
    SELECT 1 AS k, 'SC-1 Attach rate (90 days)' AS criterion, '>= 8%' AS target, channel, v AS actual, v >= 8 AS met FROM attach
    UNION ALL SELECT 2, 'SC-2 Activation within 14 days', '>= 60%', channel, activation, activation >= 60 FROM ord
    UNION ALL SELECT 3, 'SC-3 Access within 24 hours', '>= 95%', channel, within_24h, within_24h >= 95 FROM ord
    UNION ALL SELECT 4, 'SC-4 Billing error rate', '< 1%', channel, billing_error, billing_error < 1 FROM ord
)
SELECT
    criterion,
    target,
    ROUND(MAX(actual) FILTER (WHERE channel = 'overall'), 1)    AS overall_pct,
    ROUND(MAX(actual) FILTER (WHERE channel = 'self_serve'), 1) AS self_serve_pct,
    ROUND(MAX(actual) FILTER (WHERE channel = 'sales_led'), 1)  AS sales_led_pct,
    BOOL_AND(met) FILTER (WHERE channel = 'overall')            AS overall_met,
    BOOL_AND(met) FILTER (WHERE channel = 'sales_led')          AS sales_led_met
FROM long
GROUP BY k, criterion, target
ORDER BY k;
