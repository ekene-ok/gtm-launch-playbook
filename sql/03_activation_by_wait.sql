-- Does waiting for access lower activation?
-- Activation (SC-2): the account uses the add-on in the 14 days after access
SELECT
    CASE
        WHEN days_to_access <= 3  THEN '1. Within 3 days'
        WHEN days_to_access <= 7  THEN '2. 3 to 7 days'
        ELSE                           '3. Over 7 days'
    END                                           AS wait_for_access,
    COUNT(*)                                      AS orders,
    ROUND(100.0 * AVG(activated_14d::INT), 1)     AS activation_pct
FROM orders
GROUP BY 1
ORDER BY 1;
