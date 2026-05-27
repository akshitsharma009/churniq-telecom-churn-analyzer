-- Q06: Retention Action Distribution

SELECT
    bs.retention_action,
    bs.urgency,
    bs.contact_channel,
    COUNT(*)                                        AS total_customers,
    ROUND(SUM(bs.revenue_at_risk), 2)               AS total_revenue_at_risk,
    ROUND(AVG(bs.retention_roi), 2)                 AS avg_retention_roi
FROM business_summary bs
WHERE bs.is_worth_retaining = 1
GROUP BY bs.retention_action, bs.urgency, bs.contact_channel
ORDER BY total_customers DESC;