"""Olist E-Commerce ETL Pipeline — Capstone 2.

Reproducible command-line pipeline that mirrors the logic in notebooks/01_extraction.ipynb.
Reads all 9 raw Olist CSVs, cleans, merges, engineers derived columns, and exports
a single analysis-ready flat file.

Usage:
    python scripts/etl_pipeline.py \
        --input data/raw \
        --output data/processed/cleaned_olist_dataset.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Loaders
# ---------------------------------------------------------------------------

FILE_MAP = {
    "olist_orders_dataset": "orders",
    "olist_order_items_dataset": "items",
    "olist_customers_dataset": "customers",
    "olist_order_payments_dataset": "payments",
    "olist_order_reviews_dataset": "reviews",
    "olist_products_dataset": "products",
    "olist_sellers_dataset": "sellers",
    "olist_geolocation_dataset": "geolocation",
    "product_category_name_translation": "category_translation",
}


def load_all(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Load every Olist CSV from the raw directory into a dict."""
    dfs: dict[str, pd.DataFrame] = {}
    for filename, key in FILE_MAP.items():
        path = raw_dir / f"{filename}.csv"
        dfs[key] = pd.read_csv(path)
    return dfs


# ---------------------------------------------------------------------------
# 2. Cleaning helpers
# ---------------------------------------------------------------------------

DATETIME_COLUMNS: dict[str, list[str]] = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "items": ["shipping_limit_date"],
    "reviews": ["review_creation_date", "review_answer_timestamp"],
}


def parse_datetimes(dfs: dict[str, pd.DataFrame]) -> None:
    """Convert known timestamp columns to datetime (in-place)."""
    for table, cols in DATETIME_COLUMNS.items():
        for col in cols:
            dfs[table][col] = pd.to_datetime(dfs[table][col], errors="coerce")


def fix_typos(dfs: dict[str, pd.DataFrame]) -> None:
    """Fix known typos in column names and category translations."""
    dfs["products"].rename(columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length",
    }, inplace=True)

    dfs["category_translation"]["product_category_name_english"] = (
        dfs["category_translation"]["product_category_name_english"]
        .str.replace("costruction_tools_garden", "construction_tools_garden", regex=False)
        .str.replace("costruction_tools_tools", "construction_tools_tools", regex=False)
        .str.replace("fashio_female_clothing", "fashion_female_clothing", regex=False)
    )


# ---------------------------------------------------------------------------
# 3. Aggregations
# ---------------------------------------------------------------------------

def aggregate_geolocation(geo: pd.DataFrame) -> pd.DataFrame:
    """Collapse 1M geolocation rows to one row per zip code prefix."""
    agg = geo.groupby("geolocation_zip_code_prefix").agg(
        geo_lat=("geolocation_lat", "mean"),
        geo_lng=("geolocation_lng", "mean"),
        geo_city=("geolocation_city", lambda s: s.mode().iloc[0] if len(s.mode()) > 0 else np.nan),
        geo_state=("geolocation_state", lambda s: s.mode().iloc[0] if len(s.mode()) > 0 else np.nan),
    ).reset_index()
    agg["geolocation_zip_code_prefix"] = agg["geolocation_zip_code_prefix"].astype(str)
    return agg


def aggregate_payments(payments: pd.DataFrame) -> pd.DataFrame:
    """One row per order with total value, primary payment type, and max installments."""
    primary = payments[payments["payment_sequential"] == 1][
        ["order_id", "payment_type", "payment_installments"]
    ].copy()
    primary.rename(columns={
        "payment_type": "primary_payment_type",
        "payment_installments": "max_installments",
    }, inplace=True)

    totals = payments.groupby("order_id").agg(
        total_payment_value=("payment_value", "sum"),
        payment_count=("payment_sequential", "max"),
    ).reset_index()

    return totals.merge(primary, on="order_id", how="left")


def deduplicate_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    """Keep the latest review per order."""
    return (
        reviews
        .sort_values("review_answer_timestamp", ascending=False)
        .drop_duplicates(subset=["order_id"], keep="first")
        .reset_index(drop=True)
        [["order_id", "review_score", "review_creation_date", "review_answer_timestamp"]]
    )


# ---------------------------------------------------------------------------
# 4. Merge pipeline
# ---------------------------------------------------------------------------

def build_flat_table(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Chain left joins to produce the analysis-ready flat table."""
    orders = dfs["orders"]
    customers = dfs["customers"]
    items = dfs["items"]
    products = dfs["products"]
    category_translation = dfs["category_translation"]
    sellers = dfs["sellers"]
    payments_order = aggregate_payments(dfs["payments"])
    reviews_dedup = deduplicate_reviews(dfs["reviews"])

    products_en = products.merge(category_translation, on="product_category_name", how="left")
    products_en["product_category_name_english"] = (
        products_en["product_category_name_english"].fillna("uncategorised")
    )

    df = (
        orders
        .merge(customers, on="customer_id", how="left")
        .merge(items, on="order_id", how="left")
        .merge(products_en, on="product_id", how="left")
        .merge(sellers, on="seller_id", how="left", suffixes=("_customer", "_seller"))
        .merge(payments_order, on="order_id", how="left")
        .merge(reviews_dedup, on="order_id", how="left")
    )

    return df


# ---------------------------------------------------------------------------
# 5. Derived columns
# ---------------------------------------------------------------------------

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add all analytical derived columns."""
    df["delivery_delay_days"] = (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
    df["is_on_time"] = df["delivery_delay_days"] <= 0
    df["actual_delivery_days"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days

    df["purchase_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df["purchase_year"] = df["order_purchase_timestamp"].dt.year
    df["purchase_month_num"] = df["order_purchase_timestamp"].dt.month
    df["purchase_weekday"] = df["order_purchase_timestamp"].dt.day_name()
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour

    df["total_item_value"] = df["price"] + df["freight_value"]
    df["freight_ratio"] = df["freight_value"] / df["price"].replace(0, np.nan)
    df["product_volume_cm3"] = df["product_length_cm"] * df["product_height_cm"] * df["product_width_cm"]
    df["approval_lag_hours"] = (df["order_approved_at"] - df["order_purchase_timestamp"]).dt.total_seconds() / 3600

    return df


def final_cleanup(df: pd.DataFrame) -> pd.DataFrame:
    """Final housekeeping: rename, filter, cast types."""
    df.drop(columns=["product_category_name"], inplace=True, errors="ignore")
    df.rename(columns={"product_category_name_english": "product_category"}, inplace=True)

    for col in ["customer_zip_code_prefix", "seller_zip_code_prefix"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(".0", "", regex=False)

    df = df[df["order_status"] == "delivered"].copy()
    df.reset_index(drop=True, inplace=True)
    return df


# ---------------------------------------------------------------------------
# 6. Orchestrator
# ---------------------------------------------------------------------------

def run_pipeline(raw_dir: Path, output_path: Path) -> pd.DataFrame:
    """Execute the full ETL pipeline end-to-end."""
    print(f"Loading raw data from {raw_dir} ...")
    dfs = load_all(raw_dir)

    print("Parsing datetimes ...")
    parse_datetimes(dfs)

    print("Fixing typos ...")
    fix_typos(dfs)

    print("Merging tables ...")
    df = build_flat_table(dfs)

    print("Engineering features ...")
    df = engineer_features(df)

    print("Final cleanup ...")
    df = final_cleanup(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nDone → {output_path}")
    print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}  |  Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
    return df


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Olist ETL Pipeline — DVA Capstone 2")
    parser.add_argument("--input", required=True, type=Path, help="Path to data/raw/ directory")
    parser.add_argument("--output", required=True, type=Path, help="Output path for cleaned CSV")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_pipeline(args.input, args.output)
