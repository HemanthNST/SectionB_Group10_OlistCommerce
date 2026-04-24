#!/usr/bin/env python3
"""Create a Tableau-friendly sample from a large orders CSV.

The sampler keeps temporal proportions intact (year-month) and uses weighted
sampling inside each month to preserve:
- rare geographies/categories/payment types
- delivery and review edge-cases
- high-value orders
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def _normalize(values: pd.Series) -> pd.Series:
    min_v = values.min()
    max_v = values.max()
    if pd.isna(min_v) or pd.isna(max_v) or max_v == min_v:
        return pd.Series(np.zeros(len(values)), index=values.index)
    return (values - min_v) / (max_v - min_v)


def _rarity_score(series: pd.Series) -> pd.Series:
    safe = series.fillna("__MISSING__").astype(str)
    counts = safe.value_counts(dropna=False)
    freq = safe.map(counts).astype(float)
    rarity = np.log1p(freq.max()) - np.log1p(freq)
    return _normalize(rarity)


def _allocate_counts(group_sizes: pd.Series, target_n: int) -> pd.Series:
    total = int(group_sizes.sum())
    if target_n >= total:
        return group_sizes.copy()

    raw = group_sizes * (target_n / total)
    base = np.floor(raw).astype(int)

    if target_n >= len(group_sizes):
        zero_mask = (base == 0) & (group_sizes > 0)
        base.loc[zero_mask] = 1

    base = np.minimum(base, group_sizes)
    missing = target_n - int(base.sum())

    if missing > 0:
        remainders = (raw - base).sort_values(ascending=False)
        for key in remainders.index:
            if missing == 0:
                break
            if base.loc[key] < group_sizes.loc[key]:
                base.loc[key] += 1
                missing -= 1
    elif missing < 0:
        excess = -missing
        removable = (base - 1).clip(lower=0)
        order = removable.sort_values(ascending=False)
        for key in order.index:
            if excess == 0:
                break
            can_remove = min(removable.loc[key], excess)
            if can_remove > 0:
                base.loc[key] -= can_remove
                excess -= can_remove

    return base


def build_weighted_sample(df: pd.DataFrame, target_n: int, seed: int) -> pd.DataFrame:
    if target_n >= len(df):
        return df.copy()

    data = df.copy()
    data["_row_id"] = np.arange(len(data))

    state_rarity = _rarity_score(data["customer_state"])
    cat_rarity = _rarity_score(data["product_category_main"])
    pay_rarity = _rarity_score(data["primary_payment_type"])

    order_value = pd.to_numeric(data["total_order_value"], errors="coerce")
    delay_days = pd.to_numeric(data["delivery_delay_days"], errors="coerce")
    review_score = pd.to_numeric(data["review_score"], errors="coerce")

    value_thr = order_value.quantile(0.98)
    delay_hi = delay_days.quantile(0.98)
    delay_lo = delay_days.quantile(0.02)

    high_value = (order_value >= value_thr).fillna(False).astype(float)
    extreme_delay = ((delay_days >= delay_hi) | (delay_days <= delay_lo)).fillna(False).astype(float)
    low_review = (review_score <= 2).fillna(False).astype(float)

    weights = (
        1.0
        + 0.85 * cat_rarity
        + 0.55 * state_rarity
        + 0.35 * pay_rarity
        + 0.55 * high_value
        + 0.45 * extreme_delay
        + 0.35 * low_review
    )

    if "purchase_year" in data.columns and "purchase_month_num" in data.columns:
        strat_cols = ["purchase_year", "purchase_month_num"]
    elif "purchase_month" in data.columns:
        strat_cols = ["purchase_month"]
    else:
        strat_cols = []

    rng = np.random.default_rng(seed)

    if not strat_cols:
        sampled_idx = data.sample(n=target_n, replace=False, weights=weights, random_state=seed).index
        sampled_df = data.loc[sampled_idx].sort_values("_row_id")
        return sampled_df.drop(columns=["_row_id"], errors="ignore")

    group_sizes = data.groupby(strat_cols, dropna=False).size()
    allocation = _allocate_counts(group_sizes, target_n)

    sampled_indices: list[int] = []
    grouped = data.groupby(strat_cols, dropna=False)
    for group_key, group in grouped:
        n_take = int(allocation.loc[group_key])
        if n_take <= 0:
            continue

        group_w = weights.loc[group.index]
        sampled = group.sample(
            n=n_take,
            replace=False,
            weights=group_w,
            random_state=int(rng.integers(0, 1_000_000_000)),
        )
        sampled_indices.extend(sampled.index.tolist())

    sampled_df = data.loc[sampled_indices].drop(columns=["_row_id"], errors="ignore")
    sampled_df = sampled_df.sort_index()
    return sampled_df


def _print_drift_report(full_df: pd.DataFrame, sample_df: pd.DataFrame) -> None:
    print("\nQuality check (full vs sample):")

    cat_cols = ["purchase_year", "customer_state", "product_category_main", "primary_payment_type", "is_on_time"]
    for col in cat_cols:
        if col not in full_df.columns:
            continue

        p_full = full_df[col].fillna("__MISSING__").value_counts(normalize=True)
        p_samp = sample_df[col].fillna("__MISSING__").value_counts(normalize=True)
        all_levels = p_full.index.union(p_samp.index)
        drift = (p_full.reindex(all_levels, fill_value=0) - p_samp.reindex(all_levels, fill_value=0)).abs()
        print(f"- {col}: max distribution drift = {drift.max() * 100:.2f} pp")

    num_cols = ["total_order_value", "delivery_delay_days", "review_score", "actual_delivery_days"]
    for col in num_cols:
        if col not in full_df.columns:
            continue
        full_num = pd.to_numeric(full_df[col], errors="coerce")
        samp_num = pd.to_numeric(sample_df[col], errors="coerce")
        print(
            f"- {col}: "
            f"mean {full_num.mean():.2f}->{samp_num.mean():.2f}, "
            f"p50 {full_num.quantile(0.50):.2f}->{samp_num.quantile(0.50):.2f}, "
            f"p90 {full_num.quantile(0.90):.2f}->{samp_num.quantile(0.90):.2f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample Tableau orders dataset while preserving relevance.")
    parser.add_argument("--input", required=True, type=Path, help="Input CSV path")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV path")
    parser.add_argument("--target", type=int, default=20_000, help="Target row count (default: 20000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    sampled = build_weighted_sample(df, target_n=args.target, seed=args.seed)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    sampled.to_csv(args.output, index=False)

    print(f"Input rows : {len(df):,}")
    print(f"Output rows: {len(sampled):,}")
    print(f"Saved to   : {args.output}")
    _print_drift_report(df, sampled)


if __name__ == "__main__":
    main()
