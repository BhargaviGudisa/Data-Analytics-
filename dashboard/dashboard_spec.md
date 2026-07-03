# Churn Dashboard Specification

This project ships the data pipeline (`data/processed/telco_customer_churn_clean.csv`) and the SQL/Python analysis behind it. This document is the build spec for turning that output into an interactive Power BI or Tableau dashboard — connect either tool directly to the processed CSV (or the `customer_churn` SQL table) and follow the layout below.

## Data source

Connect to: `data/processed/telco_customer_churn_clean.csv`

## Page 1 — Executive Overview

| Visual | Field(s) | Notes |
|---|---|---|
| KPI card: Total Customers | `customer_id` (count) | |
| KPI card: Overall Churn Rate | `churn_flag` (average × 100) | |
| KPI card: Avg. Monthly Charges | `monthly_charges` (average) | |
| KPI card: Monthly Revenue at Risk | `monthly_charges` (sum, filtered `churn = Yes`) | |
| Donut chart: Churn Split | `churn` (count) | Retained vs Churned |
| Bar chart: Churn Rate by Contract Type | `contract` (axis), `churn_flag` (average) | Sort descending |
| Slicers | `contract`, `internet_service`, `tenure_group`, `senior_citizen` | Applies to whole page |

## Page 2 — Churn Drivers

| Visual | Field(s) | Notes |
|---|---|---|
| Bar chart: Churn Rate by Tenure Group | `tenure_group` (axis), `churn_flag` (average) | Ordered 0–12 → 61–72 mo |
| Bar chart: Churn Rate by Internet Service | `internet_service` (axis), `churn_flag` (average) | |
| Bar chart: Churn Rate by Tech Support | `tech_support` (axis), `churn_flag` (average) | |
| Scatter/density: Monthly Charges vs Churn | `monthly_charges`, `churn` (color) | |
| Table: Highest-risk segments | `contract`, `internet_service`, churn rate, customer count | Filter count ≥ 30 to avoid noisy small segments |

## Page 3 — Customer Explorer

| Visual | Field(s) | Notes |
|---|---|---|
| Table | `customer_id`, `contract`, `tenure`, `monthly_charges`, `payment_method`, `churn` | Row-level drill-through, searchable |
| Slicers | `payment_method`, `paperless_billing`, `senior_citizen` | |

## Suggested DAX / calculated measures (Power BI)

```
Churn Rate = DIVIDE(SUM(customer_churn[churn_flag]), COUNTROWS(customer_churn))
Revenue At Risk = CALCULATE(SUM(customer_churn[monthly_charges]), customer_churn[churn] = "Yes")
Avg Tenure (Churned) = CALCULATE(AVERAGE(customer_churn[tenure]), customer_churn[churn] = "Yes")
```

## Static chart reference

Until the interactive dashboard is published, static equivalents of the core visuals (generated from the same dataset via `scripts/eda_report.py`) are available in [`images/`](../images/) and referenced in the main [README](../README.md#screenshots).
