-- ============================================================
-- Schema: telco_customer_churn
-- Target: PostgreSQL / MySQL / SQLite compatible DDL
-- Loads the cleaned export produced by scripts/data_cleaning.py
-- (data/processed/telco_customer_churn_clean.csv)
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_churn (
    customer_id             VARCHAR(20)   PRIMARY KEY,
    gender                  VARCHAR(10),
    senior_citizen          VARCHAR(3),
    partner                 VARCHAR(3),
    dependents              VARCHAR(3),
    tenure                  INTEGER,
    phone_service           VARCHAR(20),
    multiple_lines          VARCHAR(20),
    internet_service        VARCHAR(20),
    online_security         VARCHAR(20),
    online_backup           VARCHAR(20),
    device_protection       VARCHAR(20),
    tech_support             VARCHAR(20),
    streaming_tv            VARCHAR(20),
    streaming_movies        VARCHAR(20),
    contract                VARCHAR(20),
    paperless_billing       VARCHAR(3),
    payment_method          VARCHAR(30),
    monthly_charges         NUMERIC(8, 2),
    total_charges           NUMERIC(10, 2),
    churn                   VARCHAR(3),
    churn_flag              SMALLINT,
    tenure_group             VARCHAR(10)
);

-- Example load (PostgreSQL):
-- \copy customer_churn FROM 'data/processed/telco_customer_churn_clean.csv' WITH (FORMAT csv, HEADER true);
