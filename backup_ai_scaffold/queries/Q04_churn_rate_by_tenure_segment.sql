-- Q04: Churn Rate by Tenure Segment

SELECT
    c.tenure_segment,
    COUNT(*)                                        AS total_customers,
    SUM(c.churn_actual)                             AS total_churned,
    ROUND(AVG(c.churn_actual) * 100, 2)             AS churn_rate_pct,
    ROUND(AVG(bs.revenue_at_risk), 2)               AS avg_revenue_at_risk
FROM customers c
JOIN business_summary bs ON c.customer_id = bs.customer_id
GROUP BY c.tenure_segment
ORDER BY churn_rate_pct DESC;