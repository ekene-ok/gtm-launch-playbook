-- Billing accuracy (SC-4): invoices that differ from the expected amount by more than 0.5%
SELECT
    order_type,
    COUNT(*)                                                         AS orders,
    SUM(CASE WHEN ABS(billed_amount - expected_amount) > 0.005 * expected_amount THEN 1 ELSE 0 END) AS billing_errors,
    ROUND(100.0 * AVG(CASE WHEN ABS(billed_amount - expected_amount) > 0.005 * expected_amount THEN 1 ELSE 0 END), 1) AS error_rate_pct
FROM orders
GROUP BY ROLLUP (order_type)
ORDER BY order_type NULLS LAST;
