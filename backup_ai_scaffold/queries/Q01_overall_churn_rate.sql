-- Q01: Overall Churn Rate
-- Shows total customers, churned count, and churn percentage

SELECT
    COUNT(*)                                        AS total_customers,
    SUM(churn_actual)                               AS total_churned,
    ROUND(AVG(churn_actual) * 100, 2)               AS churn_rate_pct
FROM customers;