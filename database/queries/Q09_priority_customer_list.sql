-- Q09: Full Priority Customer List

SELECT
    c.customer_id,
    c.contract_type,
    c.tenure_months,
    c.monthly_charges,
    cp.churn_probability,
    cp.risk_tier,
    bs.revenue_at_risk,
    bs.retention_cost,
    bs.net_retention_value,
    bs.retention_roi,
    bs.priority_score,
    bs.retention_action,
    bs.urgency,
    bs.contact_channel
FROM customers c
JOIN churn_predictions cp ON c.customer_id = cp.customer_id
JOIN business_summary bs  ON c.customer_id = bs.customer_id
WHERE bs.is_worth_retaining = 1
ORDER BY bs.priority_score DESC;