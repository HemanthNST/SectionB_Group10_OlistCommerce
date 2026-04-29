# Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue

> **Newton School of Technology | Data Visualization & Analytics — Capstone 2**
>
> End-to-end analytics case study using Python, Jupyter, GitHub, and Tableau Public to convert raw multi-table e-commerce data into decision-ready insights.

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue |
| **Sector** | E-Commerce / Retail |
| **Team ID** | Group10 |
| **Section** | Section B |
| **Faculty Mentor** | Satyaki Das |
| **Institute** | Newton School of Technology |
| **Submission Date** | 27 April 2026 |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead / PPT & Quality Lead | Hemanth Tenneti | `@HemanthTenneti` |
| Data Lead / Visualization Lead | Alisha Gupta | `@alisha-1000` |
| ETL Lead | Himanshu Pal | `@HimanshuPal29` |
| Analysis Lead | Karan Chhillar | `@kchhillar13` |
| Strategy Lead | Dhruv Kumar | `@drv-01` |
| Business Support | Vansh Khod | `@VanshKhod9` |

---

## Business Problem

Olist is a Brazilian marketplace connecting small and medium sellers to consumers across all 27 states. Between 2016 and 2018, the platform processed ~100K orders, but customer outcomes were uneven: review scores ranged from 1 to 5, delivery delays appeared regionally concentrated, and repeat purchase behavior remained weak.

The business objective is to identify the operational factors that most influence **customer satisfaction** and **revenue**, so leadership can prioritize high-impact interventions.

**Core Business Question**

> Which operational factors — delivery timeliness, seller performance, product mix, payment behavior, or geographic bottlenecks — are the strongest drivers of customer satisfaction and revenue, and where should Olist invest for maximum business impact?

**Decision Supported**

> This project supports marketplace operations leadership in allocating budgets across logistics, seller management, and category strategy using quantified evidence.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source** | Brazilian E-Commerce Public Dataset by Olist (Kaggle) |
| **Link** | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| **Volume** | ~99,441 orders, ~112,650 order items, ~100K+ payments/reviews |
| **Schema** | 9 relational tables, 55+ columns |
| **Time Period** | September 2016 — October 2018 |
| **Format** | CSV (9 files) |

**Key Analytical Columns**

| Column | Role in Analysis |
|---|---|
| `order_id` | Primary relational join key |
| `customer_state` | Regional segmentation |
| `order_purchase_timestamp` | Trend and seasonality analysis |
| `price` / `freight_value` | Revenue, AOV, freight ratio |
| `review_score` | Primary satisfaction KPI |
| `product_category_name_english` | Category performance analysis |
| `payment_type` | Payment behavior and AOV analysis |

Full schema and cleaning notes: [`docs/data_dictionary.md`](docs/data_dictionary.md)

---

## KPI Framework

| KPI | Definition | Computation |
|---|---|---|
| **Monthly Revenue (BRL)** | Total monthly transaction value | `SUM(price + freight_value)` by purchase month |
| **Average Order Value (AOV)** | Mean value per delivered order | `SUM(payment_value) / COUNT(DISTINCT order_id)` |
| **On-Time Delivery Rate** | Share of orders delivered on/before ETA | `COUNT(delivered ≤ estimated) / COUNT(delivered)` |
| **CSAT (Review Score)** | Mean review score for delivered orders | `AVG(review_score)` |
| **Repeat Purchase Rate** | Customers with 2+ orders | `COUNT(repeat_customers) / COUNT(unique_customers)` |
| **Avg Delivery Delay (days)** | Actual vs estimated delivery date | `AVG(delivered_customer_date − estimated_delivery_date)` |
| **Freight-to-Price Ratio** | Shipping cost as % of item price | `AVG(freight_value / price)` |

KPI logic implemented in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | [Tableau Public — SectionB Group10 Olist](https://public.tableau.com/app/profile/hemanth.tenneti/viz/SectionB_Group10_OlistCommerce/Overview?publish=yes) |
| **Executive View** | KPI scorecard (Revenue, AOV, CSAT, On-Time %), monthly trends, state performance |
| **Operational View** | State/category drill-downs, delivery-delay diagnostics, review-performance views |
| **Filters** | Date Range, Customer State, Product Category, Payment Type, Review Band |

Screenshots: [`tableau/screenshots/`](tableau/screenshots/) | Links: [`tableau/dashboard_links.md`](tableau/dashboard_links.md)

---

## Key Insights

1. **Delivery timeliness is the strongest driver of satisfaction.** On-time orders average ~4.2/5 vs ~2.6/5 for late orders (p < 0.001).
2. **Repeat behavior is weak (~3%).** The platform is heavily acquisition-dependent with suppressed customer lifetime value.
3. **Revenue is geographically concentrated.** SP, RJ, and MG contribute the largest revenue share — creating regional risk.
4. **High-revenue categories show satisfaction leakage.** Bulky categories (furniture, computers) underperform on reviews.
5. **Payment behavior impacts order value.** Credit card users show higher AOV than boleto/voucher segments.
6. **Freight burden is uneven.** North/Northeast states show higher freight-to-price ratios.
7. **Seasonality is significant.** Black Friday period drives major revenue spikes.
8. **Review outcomes are polarized.** Distribution is strongly bimodal (5-star and 1-star concentration).
9. **Promise adherence beats raw speed.** "Was it late?" has a stronger satisfaction effect than incremental delivery days.
10. **Customer segmentation reveals value concentration.** Small high-value segments drive disproportionate revenue.

---

## Recommendations

| # | Recommendation | Expected Impact |
|---|---|---|
| 1 | Set 95% on-time delivery SLA targets for carriers and sellers | CSAT uplift and reduction in low-score reviews |
| 2 | Launch 7-day post-purchase retention journey for first-time buyers | Higher repeat rate and revenue lift |
| 3 | Build regional logistics partnerships for underserved states | Lower freight burden and improved conversion |
| 4 | Introduce premium logistics protocol for bulky categories | Satisfaction recovery in high-revenue categories |
| 5 | Expand installment and payment campaigns for high-ticket segments | AOV increase in targeted cohorts |

---

## Repository Structure

```text
SectionB_Group10_OlistCommerce/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                          # Original dataset (never edited)
│   └── processed/                    # Cleaned output from ETL pipeline
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── scripts/
│   └── etl_pipeline.py
├── tableau/
│   ├── screenshots/
│   └── dashboard_links.md
├── reports/
│   ├── project_report.pdf
│   └── presentation.pdf
├── docs/
│   └── data_dictionary.md
├── DVA-oriented-Resume/
└── DVA-focused-Portfolio/
    └── portfolios.md
```

---

## Analytical Pipeline

1. **Define** — Scope business problem and decision lens
2. **Extract** — Load and validate all raw tables
3. **Clean & Transform** — Handle missingness, type fixes, joins, and feature engineering
4. **Analyze** — Perform EDA and statistical testing
5. **Visualize** — Publish an interactive Tableau dashboard
6. **Recommend** — Translate findings into business actions
7. **Report** — Document methodology, insights, and impact

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python + Jupyter | ETL, EDA, statistics, feature engineering |
| Pandas / NumPy | Data processing |
| SciPy / Statsmodels / Scikit-learn | Statistical testing and modeling |
| Matplotlib / Seaborn | Exploratory visual analysis |
| Tableau Public | Interactive dashboarding |
| GitHub | Collaboration and submission audit |

---

## Submission Checklist

**GitHub Repository**
- [x] Public repository follows naming convention
- [x] All notebooks committed in `.ipynb` format
- [x] `data/raw/` contains original unedited data
- [x] `data/processed/` contains cleaned outputs
- [x] `tableau/screenshots/` contains dashboard screenshots
- [x] `tableau/dashboard_links.md` contains Tableau Public URL
- [x] `docs/data_dictionary.md` completed
- [x] README includes project context, methods, and outputs
- [x] All members have visible commits and pull requests

**Tableau Dashboard**
- [x] Dashboard is published and accessible
- [x] Includes interactive filtering
- [x] Answers the core business problem

**Project Report**
- [x] Final report exported to `reports/project_report.pdf`
- [x] Problem context and methodology documented
- [x] KPI framework and analysis included
- [x] Insights and recommendations written in business language
- [x] Contribution matrix aligned with repo evidence

**Presentation Deck**
- [x] Final deck exported to `reports/presentation.pdf`
- [x] End-to-end narrative from context to impact

**Individual Assets**
- [x] DVA-oriented resume updated (`DVA-oriented-Resume/HemanthResume.pdf`)
- [x] Portfolio case study link updated (`DVA-focused-Portfolio/portfolios.md`)

---

## Contribution Matrix

This table reflects visible contribution evidence in Git history at audit time.

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
|---|---|---|---|---|---|---|---|
| Hemanth Tenneti (`@HemanthTenneti`) | Owner | Owner | Owner | Owner | Owner | Owner | Owner |
| Alisha Gupta (`@alisha-1000`) | Owner | Support | Owner | Support | Owner | Support | Support |
| Himanshu Pal (`@HimanshuPal29`) | Support | Owner | Support | Support | Support | Support | Support |
| Karan Chhillar (`@kchhillar13`) | Support | Support | Support | Owner | Support | Support | Support |
| Dhruv Kumar (`@drv-01`) | None | None | None | None | None | None | None |
| Vansh Khod (`@VanshKhod9`) | None | None | None | None | None | None | None |

_Declaration: Contribution details are intended to match verifiable GitHub evidence (commits, PRs, and file history)._

**Team Lead:** Hemanth Tenneti
**Date:** 27 April 2026

---

## Academic Integrity

All analysis, code, and recommendations in this repository are expected to be original work by the listed team members. Free-riding and misrepresentation are subject to academic penalties as per capstone policy.

---

*Newton School of Technology — Data Visualization & Analytics | Capstone 2*
