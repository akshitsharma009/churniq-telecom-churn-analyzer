-- ============================================================
-- ChurnIQ Database Schema
-- Database: SQLite
-- ============================================================

-- Drop tables if exist (clean slate)
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS churn_predictions;
DROP TABLE IF EXISTS business_summary;

-- ============================================================
-- TABLE 1: customers
-- ============================================================
CREATE TABLE customers (
    customer_id                 TEXT PRIMARY KEY,
    tenure_months               REAL,
    monthly_charges             REAL,
    contract_type               TEXT,
    payment_method              TEXT,

    -- Engineered Features
    charges_per_month_trend     REAL,
    product_to_charge_ratio     REAL,
    engagement_score            REAL,
    contract_risk_score         REAL,
    tenure_segment              TEXT,
    price_sensitivity_flag      INTEGER,
    loyalty_score               REAL,
    monthly_charge_tier         TEXT,
    support_dependency_score    REAL,
    payment_risk_flag           INTEGER,

    churn_actual                INTEGER
);

-- ============================================================
-- TABLE 2: churn_predictions
-- ============================================================
CREATE TABLE churn_predictions (
    prediction_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id         TEXT NOT NULL,
    churn_probability   REAL,
    churn_predicted     INTEGER,
    risk_tier           TEXT,
    model_version       TEXT,
    predicted_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================================
-- TABLE 3: business_summary
-- ============================================================
CREATE TABLE business_summary (
    summary_id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id                 TEXT NOT NULL,
    expected_remaining_months   REAL,
    future_revenue_loss         REAL,
    revenue_at_risk             REAL,
    retention_cost              REAL,
    net_retention_value         REAL,
    retention_roi               REAL,
    priority_score              REAL,
    is_worth_retaining          INTEGER,
    retention_action            TEXT,
    urgency                     TEXT,
    contact_channel             TEXT,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX idx_customers_contract     ON customers(contract_type);
CREATE INDEX idx_customers_tenure       ON customers(tenure_segment);
CREATE INDEX idx_predictions_customer   ON churn_predictions(customer_id);
CREATE INDEX idx_predictions_risk       ON churn_predictions(risk_tier);
CREATE INDEX idx_business_customer      ON business_summary(customer_id);
CREATE INDEX idx_business_worth         ON business_summary(is_worth_retaining);