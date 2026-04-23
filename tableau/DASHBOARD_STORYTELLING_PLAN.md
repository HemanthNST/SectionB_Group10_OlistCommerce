# Olist Tableau Storytelling Plan (Multi-Page Dashboard)

This file tells you exactly:
1) which page gets which charts,
2) what color each chart should use,
3) how to lay out the dashboard for narrative flow,
4) what optional upgrades you can do if you want fewer "basic bar charts".

---

## 1) Final Chart Inventory

You currently have **25 chart sheets total**:

- **8 KPI tiles**
  - Total Revenue
  - Total Orders
  - Repeat Order Rate
  - Avg Order Value
  - CSAT
  - On-Time Rate
  - Freight Ratio
  - Avg. Delivery Delay

- **17 analysis charts**
  1. Monthly Revenue Trend & Order Volume
  2. Top 10 States by Revenue
  3. Review Distribution
  4. Order Value Distribution
  5. Delivery Days Distribution
  6. Orders by Payment Type
  7. Top 15 Categories by Order Value
  8. Delivery Delay v. Review Score
  9. On-Time Rate v. Avg Review by State
  10. AOV v. Payment Type
  11. Category Revenue v. Customer Satisfaction
  12. On-Time Delivery Rate v. State
  13. Top 15 Categories: Revenue v. CSAT
  14. Top 10 States by Repeat Purchase
  15. Review Score Distribution by Delay
  16. Delivery Delay Distribution
  17. Monthly On-Time Rate vs CSAT

✅ You do **not** need additional charts for submission if these are done cleanly.

---

## 2) Olist Color System (Use this everywhere)

Use a consistent palette across all pages:

- **Primary (Brand Blue):** `#0052CC`
- **Secondary (Bright Blue):** `#1E90FF`
- **Accent (Gold):** `#FFB700`
- **Positive (Green):** `#10B981`
- **Negative (Red):** `#E74C3C`
- **Dark Text / Axis:** `#0F172A`
- **Light Grid / Background:** `#F5F7FB`
- **White:** `#FFFFFF`

Semantic rule:
- Revenue/volume = blue family
- On-time/good = green
- Delay/late/bad = red
- Reference/target line = gold

---

## 3) Multi-Page Storytelling Structure (Exactly what goes where)

## Page 1 — **Executive Summary (KPI + Business Health)**

### Put these sheets:
1. Total Revenue
2. Total Orders
3. Repeat Order Rate
4. Avg Order Value
5. CSAT
6. On-Time Rate
7. Freight Ratio
8. Avg. Delivery Delay
9. Monthly Revenue Trend & Order Volume
10. Top 10 States by Revenue
11. Review Distribution

### Layout:
- Row 1: 8 KPI tiles in 2 rows x 4 columns (clean cards)
- Row 2: Monthly Revenue Trend & Order Volume (full width)
- Row 3: Top 10 States by Revenue (left) + Review Distribution (right)

### Colors for this page:
- KPI numbers: Brand Blue `#0052CC`
- KPI labels: Dark text `#0F172A`
- Monthly Revenue bars: `#0052CC`
- Monthly Orders line: `#10B981`
- States by Revenue bars: `#0052CC`
- Review Distribution: 1→5 score colors:
  - 1: `#E74C3C`
  - 2: `#F97316`
  - 3: `#FFB700`
  - 4: `#84CC16`
  - 5: `#10B981`

Narrative message: “Business is growing, but quality and delivery shape customer experience.”

---

## Page 2 — **Univariate (What the data looks like individually)**

### Put these sheets:
1. Order Value Distribution
2. Delivery Days Distribution
3. Orders by Payment Type
4. Top 15 Categories by Order Value

### Layout:
- 2x2 grid
  - Top-left: Order Value Distribution
  - Top-right: Delivery Days Distribution
  - Bottom-left: Orders by Payment Type
  - Bottom-right: Top 15 Categories by Order Value

### Colors:
- Order Value Distribution histogram: `#0052CC`
- Delivery Days Distribution histogram: `#10B981`
- Orders by Payment Type:
  - credit_card `#0052CC`
  - boleto `#1E90FF`
  - debit_card `#10B981`
  - voucher `#FFB700`
- Top 15 Categories by Order Value: `#1E90FF`
- Median / threshold reference lines: `#FFB700` (dashed)

Narrative message: “Most orders are small, delivery has spread, and demand is concentrated in a few categories/payment modes.”

---

## Page 3 — **Bivariate (Relationships and drivers)**

### Put these sheets:
1. Delivery Delay v. Review Score
2. On-Time Rate v. Avg Review by State
3. AOV v. Payment Type
4. Category Revenue v. Customer Satisfaction

### Layout:
- 2x2 grid
  - Top-left: Delay v Review
  - Top-right: On-Time v Avg Review by State
  - Bottom-left: AOV v Payment Type
  - Bottom-right: Category Revenue v CSAT

### Colors:
- Delay v Review (bars): gradient red→green (`#E74C3C` to `#10B981`)
- On-Time v Avg Review (scatter): points `#0052CC` at 60% opacity + trendline `#FFB700`
- AOV v Payment Type: same payment palette as Page 2
- Category Revenue v CSAT (scatter): points `#1E90FF` at 60% opacity, platform CSAT line `#E74C3C`

Narrative message: “Delivery timeliness strongly explains satisfaction; some high-revenue categories underperform on CSAT.”

---

## Page 4 — **Geographic & Segment Performance**

### Put these sheets:
1. On-Time Delivery Rate v. State
2. Top 15 Categories: Revenue v. CSAT
3. Top 10 States by Repeat Purchase

### Layout:
- Left column (40% width): On-Time Delivery Rate v. State (full height)
- Right top (60%): Top 15 Categories: Revenue v. CSAT
- Right bottom (60%): Top 10 States by Repeat Purchase

### Filters at top (apply to all charts on this page):
- customer_state
- product_category_main
- purchase_month
- primary_payment_type

### Colors:
- On-Time Delivery Rate v State: diverging red→yellow→green
  - low `#E74C3C`
  - center `#FFB700`
  - high `#10B981`
  - 90% target line `#0F172A` dashed
- Top 15 Categories Revenue v CSAT:
  - bar length = revenue (neutral blue)
  - color = CSAT red→green
- Top 10 States by Repeat Purchase: `#10B981`

Narrative message: “Performance is uneven across states and segments; prioritize weak regions and high-revenue/low-CSAT categories.”

---

## Page 5 — **Delivery Deep-Dive (Core Business Insight)**

### Put these sheets:
1. Review Score Distribution by Delay
2. Delivery Delay Distribution
3. Monthly On-Time Rate vs CSAT

### Layout:
- Top row (full width): Review Score Distribution by Delay
- Bottom-left: Delivery Delay Distribution
- Bottom-right: Monthly On-Time Rate vs CSAT

### Filters at top:
- customer_state
- product_category_main

### Colors:
- Review Score Distribution by Delay:
  - On-Time = `#10B981`
  - Late = `#E74C3C`
- Delivery Delay Distribution histogram = `#0052CC`
  - x=0 threshold line = `#E74C3C`
- Monthly On-Time Rate vs CSAT:
  - On-Time line = `#0052CC`
  - CSAT line = `#10B981`

Narrative message: “Delivery is the strongest lever: when on-time improves, CSAT improves.”

---

## 4) Dashboard Assembly Order (Do this sequence)

1. Build all sheets (done / nearly done).
2. Create Dashboard 1 (Executive).
3. Create Dashboard 2 (Univariate).
4. Create Dashboard 3 (Bivariate).
5. Create Dashboard 4 (Geographic & Segment).
6. Create Dashboard 5 (Delivery Deep-Dive).
7. Apply consistent fonts, spacing, legend style.
8. Publish workbook to Tableau Public.
9. Add URL to `tableau/dashboard_links.md`.
10. Save screenshots for each page in `tableau/screenshots/`.

---

## 5) Why many bar charts? Could we do better?

Short answer: **yes, we can improve**.

Why bars were common:
- Bars are easiest for category comparisons (state, payment, category).
- Fast to read for evaluators.
- Lower risk of misinterpretation.

Better alternatives (optional upgrades if you have time):

1. **Top 10 States by Revenue** → Use a **filled map** (choropleth) + small bar chart inset.
2. **AOV v. Payment Type** → Use **box plot** from order-level data to show spread/outliers better.
3. **Delivery Days Distribution** → Keep histogram, add **density line** overlay for smoother shape.
4. **Category Revenue v CSAT** → Bubble chart is good; add quadrant reference lines to show action zones.

If time is limited, keep current bar-based set (it is submission-safe).

---

## 6) Final Naming Convention (Recommended)

Dashboard names:
- `1. Executive Summary`
- `2. Univariate Analysis`
- `3. Bivariate Analysis`
- `4. Geographic & Segmented Performance`
- `5. Delivery Deep-Dive`

This keeps storytelling clear and grading-friendly.

---

## 7) Final QA Checklist

- [ ] Every chart has title + readable axis labels
- [ ] Colors follow Olist palette consistently
- [ ] No overlapping labels in scatter charts
- [ ] Filters only on Page 4 and 5 (unless intentionally added)
- [ ] Number formatting correct (BRL, %, decimals)
- [ ] Same font family and spacing across all pages
- [ ] Dashboards render well in Tableau Public

---

If you want, next I can generate a **one-shot "dashboard assembly click-by-click" file** (container layout instructions with exact horizontal/vertical containers and sizing percentages).
