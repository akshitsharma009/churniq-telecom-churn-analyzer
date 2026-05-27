-- Q10: Customers Not Worth Retaining

SELECT
    c.customer_id,
    c.contract_type,
    c.tenure_months,
    c.monthly_charges,
    cp.churn_probability,
    cp.risk_tier,
    bs.revenue_at_risk,
    bs.retention_cost,
    bs.net_retention_value
FROM customers c
JOIN churn_predictions cp ON c.customer_id = cp.customer_id
JOIN business_summary bs  ON c.customer_id = bs.customer_id
WHERE bs.is_worth_retaining = 0
ORDER BY cp.churn_probability DESC;