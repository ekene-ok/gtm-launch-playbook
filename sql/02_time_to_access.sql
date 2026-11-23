-- Time from order to working access, by channel
-- Target (success criterion SC-3): 95% of orders provisioned within 24 hours
SELECT
    channel,
    COUNT(*)                                                    AS orders,
    ROUND(MEDIAN(days_to_access), 2)                            AS median_days,
    ROUND(QUANTILE_CONT(days_to_access, 0.9), 1)                AS p90_days,
    ROUND(100.0 * AVG(CASE WHEN days_to_access <= 1 THEN 1 ELSE 0 END), 1) AS pct_within_24h
FROM orders
GROUP BY ROLLUP (channel)
ORDER BY channel NULLS LAST;
