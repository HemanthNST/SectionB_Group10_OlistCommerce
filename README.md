# Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue

> **Newton School of Technology | Data Visualization & Analytics (Capstone 2)**
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
| Project Lead | Hemanth Tenneti | `@HemanthTenneti` |
| Data Lead | Alisha Gupta | `@alisha-1000` |
| ETL Lead | Himanshu Pal | `@HimanshuPal29` |
| Analysis Lead | Karan Chhillar | `@kchhillar13` |
| Visualization Lead | Alisha Gupta | `@alisha-1000` |
| Strategy Lead | Dhruv Kumar | `@drv-01` |
| PPT and Quality Lead | Hemanth Tenneti | `@HemanthTenneti` |
| Business Support | Vansh Khod | `@VanshKhod9` |

---

## Business Problem

Olist is a Brazilian marketplace connecting small and medium sellers to consumers across all 27 states. Between 2016 and 2018, the platform processed ~100K orders, but customer outcomes were uneven: review scores ranged from 1 to 5, delivery delays appeared regionally concentrated, and repeat purchase behavior remained weak.

The business objective is to identify the operational factors that most influence **customer satisfaction** and **revenue**, so leadership can prioritize high-impact interventions.

**Core Business Question**

> Which operational factors—delivery timeliness, seller performance, product mix, payment behavior, or geographic bottlenecks—are the strongest drivers of customer satisfaction and revenue, and where should Olist invest for maximum business impact?

**Decision Supported**

> This project supports marketplace operations leadership in allocating budgets across logistics, seller management, and category strategy using quantified evidence.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Brazilian E-Commerce Public Dataset by Olist (Kaggle) |
| **Direct Access Link** | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| **Data Volume** | ~99,441 orders, ~112,650 order items, ~100K+ payments/reviews |
| **Schema** | 9 relational tables, 55+ columns in total |
| **Time Period Covered** | September 2016 to October 2018 |
| **Format** | CSV |

**Key Analytical Columns**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `order_id` | Unique order identifier | Primary relational join key |
| `customer_state` | Customer state (Brazil) | Regional segmentation |
| `order_purchase_timestamp` | Order creation timestamp | Trend and seasonality analysis |
| `price` | Item price (BRL) | Revenue and pricing analysis |
| `freight_value` | Item freight (BRL) | Logistics efficiency and freight ratio |
| `review_score` | Satisfaction score (1–5) | Primary satisfaction KPI |
| `product_category_name_english` | Product category (English) | Category performance analysis |
| `payment_type` | Payment method | Payment behavior and AOV analysis |

For complete schema and cleaning notes, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| **Monthly Revenue (BRL)** | Total monthly transaction value | `SUM(price + freight_value)` by purchase month |
| **Average Order Value (AOV)** | Mean value per delivered order | `SUM(payment_value) / COUNT(DISTINCT order_id)` |
| **On-Time Delivery Rate** | Share of delivered orders on/before ETA | `COUNT(delivered <= estimated) / COUNT(delivered)` |
| **Customer Satisfaction Score (CSAT)** | Mean review score for delivered orders | `AVG(review_score)` |
| **Repeat Purchase Rate** | Customers with 2+ orders | `COUNT(repeat_customers) / COUNT(unique_customers)` |
| **Average Delivery Delay (days)** | Delivered date minus estimated date | `AVG(delivered_customer_date - estimated_delivery_date)` |
| **Freight-to-Price Ratio** | Shipping as % of item price | `AVG(freight_value / price)` |

KPI calculations are implemented in notebooks `04_statistical_analysis.ipynb` and `05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | https://public.tableau.com/app/profile/hemanth.tenneti/viz/SectionB_Group10_OlistCommerce/Overview?publish=yes |
| **Executive View** | KPI scorecard (Revenue, AOV, CSAT, On-Time %), monthly trends, state performance |
| **Operational View** | State/category drill-downs, delivery-delay diagnostics, review-performance views |
| **Main Filters** | Date Range, State, Product Category, Payment Type, Review Band |

Screenshots are available under [`tableau/screenshots/`](tableau/screenshots/) and links are documented in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

1. **Delivery timeliness is the strongest driver of satisfaction.** On-time orders average ~4.2/5 vs ~2.6/5 for late orders (p < 0.001).
2. **Repeat behavior is weak (~3% repeat customers).** The business is heavily acquisition-dependent.
3. **Revenue concentration risk exists.** SP, RJ, and MG contribute the largest revenue share.
4. **High-revenue categories show satisfaction leakage.** Bulky categories (e.g., furniture/computers) underperform on reviews.
5. **Payment behavior impacts order value.** Credit card users show higher AOV than boleto/voucher segments.
6. **Freight burden is uneven across regions.** North/Northeast states show higher freight-to-price ratios.
7. **Seasonality is significant.** Black Friday period drives major revenue spikes.
8. **Review outcomes are polarized.** Distribution is strongly bimodal (high 5-star and 1-star concentration).
9. **Promise adherence beats raw speed.** "Was it late?" has stronger satisfaction effect than incremental delivery days.
10. **Customer segmentation indicates concentration of value.** Small high-value segments drive disproportionate revenue.

---

## Recommendations

| # | Insight Addressed | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | 1, 9 | Set 95% on-time delivery SLA targets for carriers and sellers | CSAT uplift and reduction in low-score reviews |
| 2 | 2, 10 | Launch 7-day post-purchase retention journey for first-time buyers | Higher repeat rate and revenue lift |
| 3 | 3, 6 | Build regional logistics partnerships for underserved states | Lower freight burden and improved conversion |
| 4 | 4 | Introduce premium logistics protocol for bulky categories | Recovery in satisfaction for high-revenue categories |
| 5 | 5 | Expand installment/payment campaigns for high-ticket segments | AOV increase in targeted cohorts |

---

## Repository Structure

```text
SectionName_TeamID_ProjectName/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # Original dataset (never edited)
|   `-- processed/                   # Cleaned output from ETL pipeline
|
|-- notebooks/
|   |-- 01_extraction.ipynb
|   |-- 02_cleaning.ipynb
|   |-- 03_eda.ipynb
|   |-- 04_statistical_analysis.ipynb
|   `-- 05_final_load_prep.ipynb
|
|-- scripts/
|   `-- etl_pipeline.py
|
|-- tableau/
|   |-- screenshots/
|   `-- dashboard_links.md
|
|-- reports/
|   |-- README.md
|   |-- project_report.md
|   `-- presentation.md
|
|-- docs/
|   |-- data_dictionary.md
|   `-- rubric_self_assessment.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

1. **Define** — Scope business problem and decision lens.
2. **Extract** — Load and validate all raw tables.
3. **Clean & Transform** — Handle missingness, type fixes, joins, and feature engineering.
4. **Analyze** — Perform EDA and statistical testing.
5. **Visualize** — Publish an interactive Tableau dashboard.
6. **Recommend** — Translate findings into business actions.
7. **Report** — Document methodology, insights, and impact.

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

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Clarity and scope of business question |
| Data Quality & ETL | 15 | Reproducible cleaning and transformation |
| Analysis Depth | 25 | Correct and meaningful statistical analysis |
| Dashboard & Visualization | 20 | Decision-relevant interactive dashboard |
| Business Recommendations | 20 | Actionability and impact linkage |
| Storytelling & Clarity | 10 | Professional communication quality |
| **Total** | **100** | |

---

## Submission Checklist

**GitHub Repository**

- [x] Public repository follows naming convention (`SectionName_TeamID_ProjectName`)
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

- [ ] Final report exported to `reports/project_report.pdf`
- [x] Problem context and methodology documented
- [x] KPI framework and analysis included
- [x] Insights and recommendations written in business language
- [x] Contribution matrix aligned with repo evidence

**Presentation Deck**

- [ ] Final deck exported to `reports/presentation.pdf`
- [x] End-to-end narrative from context to impact

**Individual Assets**

- [ ] DVA-oriented resume updated
- [ ] Portfolio case study link updated

---

## Contribution Matrix

This table reflects visible contribution evidence in Git history/PR activity at audit time.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| Hemanth Tenneti (`@HemanthTenneti`) | Owner | Owner | Owner | Owner | Owner | Owner | Owner |
| Alisha Gupta (`@alisha-1000`) | Owner | Support | Owner | Support | Owner | Support | Support |
| Himanshu Pal (`@HimanshuPal29`) | Support | Owner | Support | Support | Support | Support | Support |
| Karan Chhillar (`@kchhillar13`) | Support | Support | Support | Owner | Support | Support | Support |
| Dhruv Kumar (`@drv-01`) | Support | Support | Support | Support | Support | Support | Support |
| Vansh Khod (`@VanshKhod9`) | Support | Support | Support | Support | Support | Support | Support |

_Declaration: Contribution details are intended to match verifiable GitHub evidence (commits, PRs, and file history)._ 

**Team Lead Name:** Hemanth Tenneti  
**Date:** 27 April 2026

---

## Academic Integrity

All analysis, code, and recommendations in this repository are expected to be original work by the listed team members. Free-riding and misrepresentation are subject to academic penalties as per capstone policy.

---

*Newton School of Technology — Data Visualization & Analytics | Capstone 2*
