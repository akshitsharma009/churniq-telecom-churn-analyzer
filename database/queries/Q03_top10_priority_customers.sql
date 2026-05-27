-- Q03: Top 10 Priority Customers
-- Highest priority score customers worth retaining

SELECT
    c.customer_id,
    c.contract_type,
    c.monthly_charges,
    cp.churn_probability,
    cp.risk_tier,
    bs.revenue_at_risk,
    bs.net_retention_value,
    bs.priority_score,
    bs.retention_action,
    bs.urgency
FROM customers c
JOIN churn_predictions cp ON c.customer_id = cp.customer_id
JOIN business_summary bs  ON c.customer_id = bs.customer_id
WHERE bs.is_worth_retaining = 1
ORDER BY bs.priority_score DESC
LIMIT 10;