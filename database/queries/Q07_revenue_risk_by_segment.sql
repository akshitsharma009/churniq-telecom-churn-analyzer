-- Q07: Revenue Risk by Segment

SELECT
    c.tenure_segment,
    c.contract_type,
    COUNT(*)                                        AS total_customers,
    ROUND(SUM(bs.future_revenue_loss), 2)           AS total_future_revenue_loss,
    ROUND(SUM(bs.revenue_at_risk), 2)               AS total_revenue_at_risk,
    ROUND(AVG(bs.revenue_at_risk), 2)               AS avg_revenue_at_risk
FROM customers c
JOIN business_summary bs ON c.customer_id = bs.customer_id
GROUP BY c.tenure_segment, c.contract_type
ORDER BY total_revenue_at_risk DESC;