-- Q05: High Risk Customers by Payment Method

SELECT
    c.payment_method,
    COUNT(*)                                        AS total_customers,
    SUM(CASE WHEN cp.risk_tier = 'HIGH' THEN 1 ELSE 0 END)    AS high_risk_count,
    ROUND(AVG(cp.churn_probability) * 100, 2)       AS avg_churn_pct,
    ROUND(SUM(bs.revenue_at_risk), 2)               AS total_revenue_at_risk
FROM customers c
JOIN churn_predictions cp ON c.customer_id = cp.customer_id
JOIN business_summary bs  ON c.customer_id = bs.customer_id
GROUP BY c.payment_method
ORDER BY high_risk_count DESC;