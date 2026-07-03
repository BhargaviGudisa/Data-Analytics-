-- ============================================================
-- Customer Churn Analysis Queries
-- Table: customer_churn (see 01_schema.sql)
-- ============================================================

-- 1. Overall churn rate
SELECT
    COUNT(*)                                              AS total_customers,
    SUM(churn_flag)                                       AS churned_customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn;

-- 2. Churn rate by contract type
SELECT
    contract,
    COUNT(*)                                              AS customers,
    SUM(churn_flag)                                       AS churned,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
GROUP BY contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn rate by internet service type
SELECT
    internet_service,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;

-- 4. Churn rate by tenure group
SELECT
    tenure_group,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
GROUP BY tenure_group
ORDER BY tenure_group;

-- 5. Impact of tech support on churn
SELECT
    tech_support,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
WHERE tech_support IN ('Yes', 'No')
GROUP BY tech_support
ORDER BY churn_rate_pct DESC;

-- 6. Average monthly / total charges: churned vs retained
SELECT
    churn,
    ROUND(AVG(monthly_charges), 2)                        AS avg_monthly_charges,
    ROUND(AVG(total_charges), 2)                          AS avg_total_charges,
    ROUND(AVG(tenure), 1)                                 AS avg_tenure_months
FROM customer_churn
GROUP BY churn;

-- 7. Top 5 highest-risk customer segments (contract x internet service)
SELECT
    contract,
    internet_service,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
GROUP BY contract, internet_service
HAVING COUNT(*) >= 30
ORDER BY churn_rate_pct DESC
LIMIT 5;

-- 8. Revenue at risk: monthly charges tied to currently churned customers
SELECT
    ROUND(SUM(monthly_charges), 2)                        AS monthly_revenue_lost_usd
FROM customer_churn
WHERE churn = 'Yes';

-- 9. Payment method vs churn rate
SELECT
    payment_method,
    COUNT(*)                                              AS customers,
    ROUND(100.0 * SUM(churn_flag) / COUNT(*), 1)          AS churn_rate_pct
FROM customer_churn
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;
