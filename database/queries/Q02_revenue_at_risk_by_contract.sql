-- Q02: Revenue At Risk by Contract Type
-- Shows revenue at risk grouped by contract type

SELECT
    c.contract_type,
    COUNT(*)                                        AS total_customers,
    ROUND(SUM(bs.revenue_at_risk), 2)               AS total_revenue_at_risk,
    ROUND(AVG(bs.revenue_at_risk), 2)               AS avg_revenue_at_risk
FROM customers c
JOIN business_summary bs
    ON c.customer_id = bs.customer_id
GROUP BY c.contract_type
ORDER BY total_revenue_at_risk DESC;