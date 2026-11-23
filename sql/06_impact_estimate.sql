-- Rough size of the prize: activations lost to waits over 3 days
-- Assumes delayed orders would have activated at the rate of orders with access within 3 days.
-- This is an estimate from observational data, not a controlled test.
WITH base AS (
    SELECT AVG(activated_14d::INT) AS rate_fast FROM orders WHERE days_to_access <= 3
),
slow AS (
    SELECT COUNT(*) AS orders, SUM(activated_14d::INT) AS activated
    FROM orders WHERE days_to_access > 3
)
SELECT
    slow.orders                                          AS orders_waiting_over_3_days,
    slow.activated                                       AS activated_actual,
    ROUND(slow.orders * base.rate_fast)                  AS activated_if_fast,
    ROUND(slow.orders * base.rate_fast) - slow.activated AS activations_lost_est
FROM slow, base;
