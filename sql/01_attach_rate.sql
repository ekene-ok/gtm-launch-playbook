-- Attach rate: share of eligible accounts that bought Harbor Assist in the first 90 days
-- Eligibility follows BR-01 (Team, Business and Enterprise plans only)
WITH eligible AS (
    SELECT account_id, channel
    FROM accounts
    WHERE plan IN ('Team', 'Business', 'Enterprise')
),
buyers AS (
    SELECT DISTINCT account_id FROM orders
)
SELECT
    e.channel,
    COUNT(*)                                        AS eligible_accounts,
    COUNT(b.account_id)                             AS buying_accounts,
    ROUND(100.0 * COUNT(b.account_id) / COUNT(*), 1) AS attach_rate_pct
FROM eligible e
LEFT JOIN buyers b USING (account_id)
GROUP BY ROLLUP (e.channel)
ORDER BY e.channel NULLS LAST;
