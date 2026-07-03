"""
Exploratory data analysis for the Telco Customer Churn dataset.

Reads the cleaned dataset from data/processed/, computes summary KPIs,
and saves chart images to images/ for use in the README and reports.

Usage:
    python scripts/eda_report.py
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_PATH = PROJECT_ROOT / "data" / "processed" / "telco_customer_churn_clean.csv"
IMAGES_DIR = PROJECT_ROOT / "images"
REPORTS_DIR = PROJECT_ROOT / "reports"

sns.set_theme(style="whitegrid")
PALETTE = {"No": "#4C72B0", "Yes": "#DD8452"}


def load_clean_data() -> pd.DataFrame:
    return pd.read_csv(CLEAN_PATH)


def compute_kpis(df: pd.DataFrame) -> dict:
    churn_rate = df["churn_flag"].mean() * 100
    avg_monthly_charges = df["monthly_charges"].mean()
    avg_tenure = df["tenure"].mean()
    month_to_month_churn = (
        df[df["contract"] == "Month-to-month"]["churn_flag"].mean() * 100
    )
    two_year_churn = df[df["contract"] == "Two year"]["churn_flag"].mean() * 100
    fiber_churn = df[df["internet_service"] == "Fiber optic"]["churn_flag"].mean() * 100
    dsl_churn = df[df["internet_service"] == "DSL"]["churn_flag"].mean() * 100
    no_tech_support_churn = df[df["tech_support"] == "No"]["churn_flag"].mean() * 100
    with_tech_support_churn = df[df["tech_support"] == "Yes"]["churn_flag"].mean() * 100

    return {
        "total_customers": int(len(df)),
        "overall_churn_rate_pct": round(churn_rate, 1),
        "avg_monthly_charges_usd": round(avg_monthly_charges, 2),
        "avg_tenure_months": round(avg_tenure, 1),
        "month_to_month_churn_rate_pct": round(month_to_month_churn, 1),
        "two_year_contract_churn_rate_pct": round(two_year_churn, 1),
        "fiber_optic_churn_rate_pct": round(fiber_churn, 1),
        "dsl_churn_rate_pct": round(dsl_churn, 1),
        "no_tech_support_churn_rate_pct": round(no_tech_support_churn, 1),
        "with_tech_support_churn_rate_pct": round(with_tech_support_churn, 1),
    }


def plot_churn_by_contract(df: pd.DataFrame) -> None:
    rate = (
        df.groupby("contract")["churn_flag"].mean().mul(100).sort_values()
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rate.plot(kind="barh", color="#4C72B0", ax=ax)
    ax.set_xlabel("Churn rate (%)")
    ax.set_ylabel("")
    ax.set_title("Churn Rate by Contract Type")
    for i, v in enumerate(rate):
        ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_by_contract.png", dpi=150)
    plt.close(fig)


def plot_churn_by_tenure_group(df: pd.DataFrame) -> None:
    rate = df.groupby("tenure_group", observed=True)["churn_flag"].mean().mul(100)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rate.plot(kind="bar", color="#DD8452", ax=ax)
    ax.set_ylabel("Churn rate (%)")
    ax.set_xlabel("Tenure group")
    ax.set_title("Churn Rate by Customer Tenure")
    plt.xticks(rotation=0)
    for i, v in enumerate(rate):
        ax.text(i, v + 0.5, f"{v:.1f}%", ha="center")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_by_tenure.png", dpi=150)
    plt.close(fig)


def plot_monthly_charges_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.kdeplot(
        data=df, x="monthly_charges", hue="churn", fill=True,
        common_norm=False, palette=PALETTE, ax=ax,
    )
    ax.set_title("Monthly Charges Distribution: Churned vs Retained")
    ax.set_xlabel("Monthly charges (USD)")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "monthly_charges_distribution.png", dpi=150)
    plt.close(fig)


def plot_churn_by_internet_service(df: pd.DataFrame) -> None:
    rate = (
        df.groupby("internet_service")["churn_flag"].mean().mul(100).sort_values()
    )
    fig, ax = plt.subplots(figsize=(7, 4.5))
    rate.plot(kind="barh", color="#55A868", ax=ax)
    ax.set_xlabel("Churn rate (%)")
    ax.set_ylabel("")
    ax.set_title("Churn Rate by Internet Service Type")
    for i, v in enumerate(rate):
        ax.text(v + 0.5, i, f"{v:.1f}%", va="center")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "churn_by_internet_service.png", dpi=150)
    plt.close(fig)


def plot_overall_churn_split(df: pd.DataFrame) -> None:
    counts = df["churn"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        colors=[PALETTE.get(k, "#999999") for k in counts.index],
        startangle=90,
    )
    ax.set_title("Overall Customer Churn Split")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "overall_churn_split.png", dpi=150)
    plt.close(fig)


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_clean_data()
    kpis = compute_kpis(df)

    plot_churn_by_contract(df)
    plot_churn_by_tenure_group(df)
    plot_monthly_charges_distribution(df)
    plot_churn_by_internet_service(df)
    plot_overall_churn_split(df)

    kpi_path = REPORTS_DIR / "kpi_summary.json"
    kpi_path.write_text(json.dumps(kpis, indent=2))

    print("KPI summary:")
    for k, v in kpis.items():
        print(f"  {k}: {v}")
    print(f"\nSaved charts to {IMAGES_DIR.relative_to(PROJECT_ROOT)}/")
    print(f"Saved KPI summary to {kpi_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
