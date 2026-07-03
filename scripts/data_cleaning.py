"""
Data cleaning pipeline for the Telco Customer Churn dataset.

Reads the raw export from data/raw/, applies type fixes and cleaning rules,
and writes an analysis-ready CSV to data/processed/.

Usage:
    python scripts/data_cleaning.py
"""

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "telco_customer_churn.csv"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "telco_customer_churn_clean.csv"


def load_raw_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw Telco churn export."""
    return pd.read_csv(path)


def clean_customer_churn(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning rules to the raw churn dataset.

    Steps:
        1. Standardize column names to snake_case.
        2. Coerce TotalCharges to numeric (11 rows ship as blank strings
           for customers with 0 tenure) and drop the unresolvable rows.
        3. Cast SeniorCitizen from 0/1 to Yes/No for readability.
        4. Convert Churn to a boolean flag for aggregation.
        5. Drop the customer_id column from modeling-ready output but
           keep it for joins/lookups.
        6. Bucket tenure into cohort groups used throughout the EDA.
    """
    df = df.copy()
    df.columns = (
        df.columns.str.replace(r"(?<!^)(?=[A-Z])", "_", regex=True).str.lower()
    )
    df = df.rename(columns={"customer_i_d": "customer_id"})

    df["total_charges"] = pd.to_numeric(df["total_charges"], errors="coerce")
    df = df.dropna(subset=["total_charges"]).reset_index(drop=True)

    df["senior_citizen"] = df["senior_citizen"].map({0: "No", 1: "Yes"})

    df["churn_flag"] = (df["churn"] == "Yes").astype(int)

    df["tenure_group"] = pd.cut(
        df["tenure"],
        bins=[0, 12, 24, 48, 60, 72],
        labels=["0-12 mo", "13-24 mo", "25-48 mo", "49-60 mo", "61-72 mo"],
        include_lowest=True,
    )

    return df


def main() -> None:
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_df = load_raw_data()
    clean_df = clean_customer_churn(raw_df)
    clean_df.to_csv(PROCESSED_PATH, index=False)
    print(f"Cleaned {len(raw_df)} raw rows -> {len(clean_df)} clean rows")
    print(f"Saved to {PROCESSED_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
