-- Q08: Retention ROI by Segment

SELECT
    c.contract_type,
    c.tenure_segment,
    COUNT(*)                                        AS total_customers,
    ROUND(AVG(bs.retention_roi), 2)                 AS avg_retention_roi,
    ROUND(SUM(bs.net_retention_value), 2)           AS total_net_retention_value,
    ROUND(SUM(bs.retention_cost), 2)                AS total_retention_cost
FROM customers c
JOIN business_summary bs ON c.customer_id = bs.customer_id
WHERE bs.is_worth_retaining = 1
GROUP BY c.contract_type, c.tenure_segment
ORDER BY avg_retention_roi DESC;