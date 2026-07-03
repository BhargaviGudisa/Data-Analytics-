# Key Findings — Telco Customer Churn Analysis

Generated from `data/processed/telco_customer_churn_clean.csv` (7,032 customers) via `scripts/eda_report.py` and `sql/02_churn_analysis_queries.sql`. Full KPI values: [`kpi_summary.json`](kpi_summary.json).

## Headline numbers

- **Overall churn rate: 26.6%** — roughly 1 in 4 customers churned.
- **Monthly revenue at risk:** charges tied to currently churned customers total **$139,131/mo** (query 8 in `sql/02_churn_analysis_queries.sql`).
- Average customer tenure is **32.4 months**; average monthly charge is **$64.80**.

## Churn drivers

1. **Contract type is the strongest signal.** Month-to-month customers churn at **42.7%**, versus **2.8%** for two-year contracts — a ~15x gap. One-year contracts sit in between.
2. **Early tenure is the highest-risk period.** Churn is concentrated in the first 12 months and declines steadily as tenure increases.
3. **Fiber optic customers churn more than DSL.** Fiber churns at **41.9%** vs **19.0%** for DSL, despite fiber being the higher-margin product — worth investigating service quality or price sensitivity.
4. **Tech support reduces churn substantially.** Customers without tech support churn at **41.6%**, vs **15.2%** for those with it — a ~2.7x difference.
5. **Highest-risk segment:** month-to-month contract + fiber optic internet customers show the highest combined churn rate among segments with meaningful sample size (see query 7).

## Business recommendations

- **Incentivize contract upgrades.** Target month-to-month, fiber-optic customers in their first 12 months with discounted 1-year or 2-year contract offers — this is the single highest-leverage segment.
- **Bundle tech support into fiber plans**, at least for the first year, to offset the elevated fiber churn rate.
- **Build a first-90-days retention track** (onboarding check-ins, proactive support outreach) given how strongly early tenure predicts churn.
- **Audit fiber service quality and pricing** relative to DSL, since the churn gap suggests a product-experience or price-sensitivity issue rather than just contract flexibility.
