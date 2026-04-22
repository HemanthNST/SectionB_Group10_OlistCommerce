# Tableau Dashboard Build Guide

*This document describes exactly what to build in Tableau Public. The data files are ready in `data/processed/`.*

---

## Data Source

**Primary file**: `data/processed/tableau_orders_kpi.csv` (19.9 MB, ~96K rows, 24 columns)

This is the main order-level file with all KPIs pre-computed. Load it as your primary data source in Tableau.

**Optional supplement files** (pre-aggregated for quick charts):
- `tableau_state_kpi.csv` — one row per Brazilian state
- `tableau_category_kpi.csv` — one row per product category
- `tableau_monthly_kpi.csv` — one row per month
- `tableau_payment_kpi.csv` — one row per payment type

---

## Dashboard 1: Executive View

**Purpose**: Give leadership a 30-second snapshot of platform health.

### Layout (top to bottom)

**Row 1 — KPI Scorecard (4 number tiles across the top)**
| Tile | Measure | Format |
|---|---|---|
| Total Revenue | SUM(total_payment) | BRL #,##0.0M |
| Avg Order Value | AVG(total_payment) | BRL #,##0 |
| CSAT Score | AVG(review_score) | #.00 / 5 |
| On-Time % | AVG(is_on_time) — use SUM(is_on_time)/COUNT(orders) | #.#% |

**Row 2 — Monthly Revenue Trend (line chart)**
- Columns: purchase_month (continuous)
- Rows: SUM(total_payment)
- Colour: single colour
- Add a dual-axis for order count (SUM(Number of Records))

**Row 3 — Two charts side by side**
- **Left**: Top 10 States by Revenue (horizontal bar, SUM(total_payment) by customer_state)
- **Right**: Review Score Distribution (bar chart, COUNT by review_score 1-5, coloured by score)

---

## Dashboard 2: Operational View

**Purpose**: Let operations managers drill into problems by region, category, and delivery performance.

### Layout

**Row 1 — Filters (across the top)**
- Customer State (dropdown filter)
- Product Category (dropdown filter)
- Payment Type (dropdown filter)
- Purchase Month (range slider)

**Row 2 — Three charts**
- **Left**: On-Time Delivery Rate by State (horizontal bar, on_time_rate by customer_state, coloured red/green)
- **Center**: Avg Review Score by Category (bar chart, top 15 categories by revenue, coloured by avg_review — red < 3.8, yellow 3.8-4.1, green > 4.1)
- **Right**: Payment Type Breakdown (pie or donut chart, COUNT by primary_payment_type)

**Row 3 — Two charts**
- **Left**: Delivery Delay vs Review Score (scatter plot, AVG(delivery_delay_days) vs AVG(review_score) by customer_state, sized by order count)
- **Right**: Monthly CSAT + On-Time Rate trend (dual-axis line chart)

---

## Interactive Filters (Mandatory per Rubric)

All filters on the Operational View should be set to **"Apply to all worksheets using this data source"** so they cascade across every chart.

At minimum, include:
1. **Date Range** (purchase_month)
2. **Customer State**
3. **Product Category**
4. **Payment Type**

---

## Build Steps

1. **Open Tableau Public** → Connect → To File → Select `tableau_orders_kpi.csv`
2. **Set data types**: Ensure `purchase_date` is recognised as Date, `review_score` as Whole Number, `is_on_time` as Boolean
3. **Build Dashboard 1** (Executive View) as a new dashboard
4. **Build Dashboard 2** (Operational View) as a second dashboard
5. **Add filters** to Dashboard 2, set to apply to all
6. **Publish**: Server → Tableau Public → Save as "Olist Marketplace Analytics"
7. **Copy the public URL** → paste into `tableau/dashboard_links.md`
8. **Take screenshots** of both dashboards → save to `tableau/screenshots/` as `executive_view.png` and `operational_view.png`

---

## Key Calculated Fields (if needed)

| Field Name | Formula |
|---|---|
| On-Time Rate | `SUM([is_on_time]) / COUNT([order_id])` |
| Revenue (M BRL) | `SUM([total_payment]) / 1000000` |
| Freight Ratio | `SUM([total_freight]) / SUM([total_items_price])` |
| Review Band | `IF [review_score] >= 4 THEN "Positive" ELSEIF [review_score] <= 2 THEN "Negative" ELSE "Neutral" END` |

---

## What to Avoid

- ❌ No pie charts for >5 categories
- ❌ No 3D charts
- ❌ No hardcoded numbers — everything must be calculated fields
- ❌ Don't use colour just for decoration — colour should encode meaning (e.g., red = bad, green = good)
- ❌ Don't clutter — white space is your friend
