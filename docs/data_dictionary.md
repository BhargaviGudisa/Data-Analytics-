# Data Dictionary — Telco Customer Churn

Source: raw export at `data/raw/telco_customer_churn.csv` (7,043 rows, 21 columns). Cleaned/derived columns are produced by `scripts/data_cleaning.py` into `data/processed/telco_customer_churn_clean.csv` (7,032 rows).

| Column (clean) | Raw column | Type | Description |
|---|---|---|---|
| `customer_id` | `customerID` | string | Unique customer identifier |
| `gender` | `gender` | string | Male / Female |
| `senior_citizen` | `SeniorCitizen` | string | Yes / No (recoded from 1/0 for readability) |
| `partner` | `Partner` | string | Whether the customer has a partner |
| `dependents` | `Dependents` | string | Whether the customer has dependents |
| `tenure` | `tenure` | integer | Months the customer has stayed with the company |
| `phone_service` | `PhoneService` | string | Whether the customer has phone service |
| `multiple_lines` | `MultipleLines` | string | Yes / No / No phone service |
| `internet_service` | `InternetService` | string | DSL / Fiber optic / No |
| `online_security` | `OnlineSecurity` | string | Yes / No / No internet service |
| `online_backup` | `OnlineBackup` | string | Yes / No / No internet service |
| `device_protection` | `DeviceProtection` | string | Yes / No / No internet service |
| `tech_support` | `TechSupport` | string | Yes / No / No internet service |
| `streaming_tv` | `StreamingTV` | string | Yes / No / No internet service |
| `streaming_movies` | `StreamingMovies` | string | Yes / No / No internet service |
| `contract` | `Contract` | string | Month-to-month / One year / Two year |
| `paperless_billing` | `PaperlessBilling` | string | Yes / No |
| `payment_method` | `PaymentMethod` | string | Electronic check / Mailed check / Bank transfer (auto) / Credit card (auto) |
| `monthly_charges` | `MonthlyCharges` | float | Current monthly charge (USD) |
| `total_charges` | `TotalCharges` | float | Total amount charged to date (USD); coerced to numeric, 11 blank rows dropped |
| `churn` | `Churn` | string | Yes / No — whether the customer left within the last month |
| `churn_flag` | *(derived)* | integer | 1 if `churn == "Yes"`, else 0 — used for aggregation |
| `tenure_group` | *(derived)* | category | Tenure bucketed into `0-12 mo`, `13-24 mo`, `25-48 mo`, `49-60 mo`, `61-72 mo` |

## Known data quality notes

- 11 rows (0.16%) had a blank `TotalCharges` value in the raw export; all had `tenure = 0` (new customers not yet billed). These rows are dropped during cleaning rather than imputed, since there is no reliable value to infer.
- `SeniorCitizen` ships as `0`/`1` in the raw file while every other flag column uses `Yes`/`No`; this is standardized during cleaning.
