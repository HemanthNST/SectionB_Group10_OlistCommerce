# Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue

## Project Report

**Sector**: E-Commerce / Retail (Brazil)

**Team ID**: _To be filled_

**Institute**: Newton School of Technology

**Faculty Mentor**: _To be filled_

**Submission Date**: _To be filled_

---

## 1. Cover Page

**Project Title**: Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue

**Program**: Data Visualization & Analytics — Capstone 2

**Institute**: Newton School of Technology

**Team Members**:

| Role | Name | GitHub |
|---|---|---|
| Project Lead | Hemanth Tenneti | @HemanthTenneti |
| Data Lead | _Name_ | _handle_ |
| ETL Lead | _Name_ | _handle_ |
| Analysis Lead | _Name_ | _handle_ |
| Visualization Lead | _Name_ | _handle_ |
| Strategy Lead | _Name_ | _handle_ |
| PPT and Quality Lead | _Name_ | _handle_ |

---

## 2. Executive Summary

This project analyses the Brazilian Olist e-commerce marketplace dataset (~99K orders, 2016–2018) to identify which operational levers — delivery timeliness, seller quality, product mix, pricing, and payment behaviour — most influence customer satisfaction and revenue.

**Key findings**: Delivery timeliness is the single strongest driver of customer satisfaction (on-time orders score 4.2/5 vs 2.6/5 for late, Cohen's d > 0.8). Only 3% of customers return, making retention the largest growth lever. Revenue is geographically concentrated in SP/RJ/MG, and high-revenue categories like furniture and computers suffer from below-average satisfaction.

**Recommendations**: (1) Set 95% on-time delivery targets in carrier SLAs. (2) Launch 7-day post-purchase nurture sequences. (3) Establish regional logistics partnerships to reduce freight costs in Northern/Northeastern states. (4) Create premium logistics tiers for bulky categories. (5) Partner with card issuers for zero-interest instalment campaigns.

---

## 3. Sector and Business Context

Olist operates as a marketplace platform connecting small and medium sellers to consumers across all 27 Brazilian states. The Brazilian e-commerce market grew significantly during 2016-2018, but marketplace logistics remain challenging due to Brazil's continental geography, uneven infrastructure, and fragmented carrier networks.

The key stakeholder for this analysis is Olist's VP of Marketplace Operations, who needs to allocate improvement budgets across logistics, seller management, and category strategy with quantified evidence rather than intuition.

---

## 4. Problem Statement and Objectives

**Core question**: Which operational factors — delivery timeliness, seller performance, product category mix, payment behaviour, or geographic bottlenecks — are the strongest drivers of customer satisfaction and revenue, and where should Olist invest resources to maximise impact?

**Objectives**:
1. Build a reproducible Python ETL pipeline from 9 relational CSVs
2. Perform exploratory and statistical analysis to identify satisfaction drivers
3. Segment customers by value and behaviour (RFM + k-means)
4. Quantify the relationship between delivery performance and reviews
5. Deliver an interactive Tableau dashboard and 5 actionable recommendations

---

## 5. Data Description

| Attribute | Details |
|---|---|
| **Source** | Brazilian E-Commerce Public Dataset by Olist (Kaggle) |
| **URL** | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| **Tables** | 9 relational CSVs |
| **Total orders** | ~99,441 |
| **Total order items** | ~112,650 |
| **Columns** | 55+ across all tables |
| **Time coverage** | September 2016 – October 2018 |
| **Format** | CSV |

**Key quality issues identified**:
- Portuguese category names requiring translation
- ~1M geolocation rows needing aggregation
- Multiple payments per order requiring consolidation
- Column name typos in products table (`lenght` → `length`)
- ~827 orders missing review scores
- Category translation typos (`costruction` → `construction`)

---

## 6. Cleaning and Transformation Methodology

The ETL pipeline (Notebook 01 + `scripts/etl_pipeline.py`) performs these steps:

1. **Load all 9 CSVs** into a dictionary of dataframes
2. **Fix typos**: Column names (`lenght` → `length`) and category translations (`costruction` → `construction`, `fashio` → `fashion`)
3. **Parse 8 datetime columns** across orders, items, and reviews tables
4. **Aggregate geolocation**: 1,000,163 rows → 19,015 rows (mean lat/lng per zip code prefix)
5. **Aggregate payments**: Multiple sequential payments per order → single row per order with total value and primary payment type
6. **De-duplicate reviews**: Keep latest review per order based on `review_answer_timestamp`
7. **Merge all tables**: Left joins starting from orders backbone → customers → items → products → sellers → payments → reviews
8. **Filter to delivered orders only**: Removes ~6% non-delivered orders for cleaner analysis
9. **Engineer 12 derived columns**: `delivery_delay_days`, `is_on_time`, `actual_delivery_days`, `purchase_month/year/hour/weekday`, `total_item_value`, `freight_ratio`, `product_volume_cm3`, `approval_lag_hours`

**Output**: 110,197 rows × 48 columns in `data/processed/cleaned_olist_dataset.csv`

---

## 7. KPI Framework

| KPI | Value | Formula |
|---|---|---|
| **Total Revenue** | BRL 15.3M | SUM(total_payment_value) |
| **Average Order Value** | BRL 160.58 | SUM(payment) / COUNT(orders) |
| **On-Time Delivery Rate** | 93.4% | COUNT(delivered ≤ estimated) / COUNT(delivered) |
| **CSAT (Avg Review Score)** | 4.08 / 5 | AVG(review_score) |
| **Repeat Purchase Rate** | 3.0% | COUNT(customers with ≥2 orders) / COUNT(unique customers) |
| **Avg Delivery Delay** | -11.2 days | AVG(delivered − estimated) — negative means early |
| **Platform Freight Ratio** | 19.8% | SUM(freight) / SUM(price) |

---

## 8. Exploratory Analysis — Key Findings

**Revenue & Volume**: Revenue nearly doubled from Jan 2017 to Nov 2017, with a sharp Black Friday spike. Peak ordering occurs weekdays 10am-4pm; weekends drop ~40%.

**Geography**: São Paulo alone accounts for ~40% of revenue. The top 3 states (SP, RJ, MG) dominate, creating regional concentration risk.

**Product Categories**: Health & beauty leads in volume; watches & gifts leads in average price. Several high-revenue categories (furniture, computers) have below-average satisfaction scores.

**Delivery & Satisfaction**: Most orders arrive early (median delay = -10 days), but the late-delivery tail clusters at 1-15 days past estimate. Late deliveries are strongly associated with score-1 reviews. The relationship is visible in box plots and confirmed by statistical tests.

**Payment**: Credit card accounts for ~75% of orders with the highest AOV. 50%+ of credit card users pay in 3+ instalments. Boleto represents a large segment with lower AOV.

**Pricing**: 15% of orders have freight exceeding 50% of item price. Northern/Northeastern states bear 2x the freight ratio of Southeast states.

---

## 9. Statistical Analysis Results

### Test 1: Correlation Analysis
Spearman correlation shows `delivery_delay_days` has the strongest negative correlation with review score (ρ ≈ -0.30). Payment and price features show near-zero correlation, confirming that delivery experience dominates satisfaction.

### Test 2: Welch's t-test — On-Time vs Late Reviews
- On-time mean: 4.21 | Late mean: 2.64 | Cohen's d > 0.8 (large effect)
- **Result**: Reject H₀ (p < 0.001). Late deliveries crater satisfaction.

### Test 3: ANOVA — Payment Type vs Order Value
- Credit card AOV ≈ BRL 170, voucher ≈ BRL 65
- **Result**: Reject H₀ (p < 0.001). Payment type significantly influences spend.

### Test 4: Chi-Squared — Review Score vs On-Time Delivery
- Cramér's V ≈ 0.30 (moderate-strong association)
- **Result**: Reject H₀. Review score distribution is fundamentally different for on-time vs late orders.

### Test 5: OLS Regression — Predicting Review Score
- `is_late` has the largest negative coefficient; `total_payment` is near zero
- R² is modest, meaning unmeasured factors (product quality, packaging) also contribute

### Test 6: RFM + K-Means Segmentation (k=4)
- **Champions** (<5%): Repeat buyers with highest spend
- **Recent / New** (bulk): Single-purchase customers needing nurture
- **Loyal**: Multi-order customers worth retaining with VIP perks
- **At-Risk / Dormant**: Haven't returned; need win-back campaigns

---

## 10. Dashboard Walkthrough

*To be completed after Tableau Public dashboard is built. Screenshots will be added to `tableau/screenshots/`.*

**Executive View**: KPI scorecard showing Revenue, AOV, CSAT, On-Time %, with monthly trend lines.

**Operational View**: Drill-down by state → category → payment type, with delivery delay heatmap, review vs delay scatter plot, and category performance matrix.

**Filters**: Date range, Customer State, Product Category, Payment Type, Review Score Band.

---

## 11. Key Insights

1. Delivery timeliness is the single strongest driver of customer satisfaction (on-time: 4.2/5 vs late: 2.6/5, p < 0.001).
2. Only 3% of customers return — the platform runs an acquisition-only model with suppressed lifetime value.
3. Revenue is geographically concentrated in SP/RJ/MG, creating regional risk.
4. High-revenue categories (furniture, computers, appliances) have below-average satisfaction.
5. Credit card instalment users have the highest AOV (~BRL 170); boleto users are underserved.
6. 15% of orders have freight > 50% of item price, especially in Northern/Northeastern states.
7. Revenue nearly doubled Jan-Nov 2017 with heavy Black Friday seasonality; non-seasonal months dip.
8. Review scores are bimodal — love-it (5) or hate-it (1) — with very little middle ground.
9. Meeting delivery estimates matters more to customers than raw delivery speed.
10. RFM clustering shows Champions (<5% of base) drive disproportionate revenue; the nurture window is 7 days post-purchase.

---

## 12. Recommendations

| # | Recommendation | Linked Insight | Expected Impact |
|---|---|---|---|
| 1 | Set 95% on-time delivery target in carrier/seller SLAs | 1, 9 | CSAT +0.3-0.5 pts; 10-15% fewer score-1 reviews |
| 2 | Launch 7-day post-purchase nurture sequence | 2, 10 | +2-3pp repeat rate → 15-20% revenue lift |
| 3 | Regional carrier partnerships / forward warehouses in North/Northeast | 3, 6 | 15-20% freight reduction; improved regional conversion |
| 4 | Premium logistics tier for bulky/fragile categories | 4 | +0.3-0.5 CSAT in high-rev categories; protects BRL 2M+ |
| 5 | Zero-interest instalment partnerships + boleto bundles | 5 | +8-12% AOV for boleto; higher instalment-eligible conversion |

---

## 13. Limitations and Next Steps

**Data limitations**:
- Dataset covers 2016-2018 only; may not reflect current Olist operations
- Customer demographic data is absent (age, gender, income)
- Seller-side economics (margins, commissions) are not included
- Review text is mostly in Portuguese and highly sparse (~58% null)

**Method limitations**:
- RFM segmentation is basic; more sophisticated churn models (e.g., BG/NBD) could improve predictions
- OLS regression R² is modest — unmeasured factors (product quality, seller communication) matter
- Causal inference is limited; correlations do not prove causation

**Suggested future work**:
- Predictive churn model using machine learning (gradient boosting)
- Seller performance scoring system
- A/B testing framework for delivery estimate accuracy
- NLP analysis on Portuguese review text for sentiment extraction

---

## 14. Contribution Matrix

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
|---|---|---|---|---|---|---|---|
| Hemanth Tenneti | Owner | Owner | Owner | Owner | Support | Owner | Owner |
| _Member 2_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ |
| _Member 3_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ |
| _Member 4_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ |
| _Member 5_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ |
| _Member 6_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ | _Owner / Support_ |

*Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts.*
