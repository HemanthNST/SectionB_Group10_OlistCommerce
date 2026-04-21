# DVA Capstone 2 - Project Repository

> **Data Visualization & Analytics**
> A 2-week industry simulation capstone using Python, GitHub, and Tableau to convert raw data into actionable business intelligence.

---

## Before You Start

1. Rename the repository using the format `SectionName_TeamID_ProjectName`.
2. Fill in the project details and team table below.
3. Add the raw dataset to `data/raw/`.
4. Complete the notebooks in order from `01` to `05`.
5. Publish the final dashboard and add the public link in `tableau/dashboard_links.md`.
6. Export the final report and presentation as PDFs into `reports/`.

### Quick Start

If you are working locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

If you are working in Google Colab:

- Upload or sync the notebooks from `notebooks/`
- Keep the final `.ipynb` files committed to GitHub
- Export any cleaned datasets into `data/processed/`

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue |
| **Sector** | E-Commerce / Retail |
| **Team ID** | _e.g. DVA-B1-T3_ |
| **Section** | _To be filled by team_ |
| **Faculty Mentor** | _To be filled by team_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | _To be filled by team_ |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | Hemanth Tenneti | `@HemanthTenneti` |
| Data Lead |  | `github-handle` |
| ETL Lead |  | `github-handle` |
| Analysis Lead |  | `github-handle` |
| Visualization Lead |  | `github-handle` |
| Strategy Lead |  | `github-handle` |
| PPT and Quality Lead |  | `github-handle` |

---

## Business Problem

Olist is a Brazilian marketplace that connects small-and-medium sellers to consumers across all 27 states. Between 2016 and 2018 the platform processed ~100K orders, but not all transactions resulted in happy customers — review scores span 1 to 5, delivery delays are common in certain regions, and repeat purchase behaviour is unclear. The leadership team needs to understand which operational levers (delivery speed, seller quality, product mix, pricing, and payment experience) most influence customer satisfaction and revenue, so they can prioritise fixes that have the highest business impact.

**Core Business Question**

> Which operational factors — delivery timeliness, seller performance, product category mix, payment behaviour, or geographic bottlenecks — are the strongest drivers of customer satisfaction and revenue, and where should Olist invest resources to maximise impact?

**Decision Supported**

> This analysis enables Olist's VP of Marketplace Operations to allocate improvement budgets across logistics, seller management, and category strategy with quantified evidence rather than intuition.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Brazilian E-Commerce Public Dataset by Olist (Kaggle) |
| **Direct Access Link** | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| **Row Count** | ~99,441 orders, ~112,650 order items, ~100K+ payments/reviews |
| **Column Count** | 9 relational tables totalling 55+ columns |
| **Time Period Covered** | September 2016 to October 2018 |
| **Format** | CSV (9 files) |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `order_id` | Unique order identifier | Primary join key across all tables |
| `customer_state` | Brazilian state of the customer | Geographic segmentation, regional analysis |
| `order_purchase_timestamp` | When the order was placed | Time-series trends, seasonality |
| `price` | Item price in BRL | Revenue, AOV, price-satisfaction analysis |
| `freight_value` | Shipping cost per item | Freight-to-price ratio, logistics efficiency |
| `review_score` | Customer satisfaction rating (1–5) | Target variable for satisfaction drivers |
| `product_category_name_english` | Product category in English | Category-level profitability and satisfaction |
| `payment_type` | Payment method (credit_card, boleto, etc.) | Payment behaviour and order value analysis |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| **Monthly Revenue (BRL)** | Total transaction value per calendar month | `SUM(price + freight_value)` grouped by `order_purchase_timestamp` month |
| **Average Order Value (AOV)** | Mean revenue per completed order | `SUM(payment_value) / COUNT(DISTINCT order_id)` where `order_status = 'delivered'` |
| **On-Time Delivery Rate** | % of orders delivered on or before estimated date | `COUNT(delivered ≤ estimated) / COUNT(delivered)` × 100 |
| **Customer Satisfaction Score (CSAT)** | Mean review score across all delivered orders | `AVG(review_score)` where `order_status = 'delivered'` |
| **Repeat Purchase Rate** | % of customers who placed 2+ orders | `COUNT(customer_unique_id with ≥2 orders) / COUNT(DISTINCT customer_unique_id)` × 100 |
| **Avg Delivery Delay (days)** | Mean difference between actual and estimated delivery | `AVG(delivered_customer_date - estimated_delivery_date)` in days |
| **Freight-to-Price Ratio** | Shipping cost as proportion of item price | `AVG(freight_value / price)` per order; flag if > 0.5 |

Document KPI logic clearly in `notebooks/04_statistical_analysis.ipynb` and `notebooks/05_final_load_prep.ipynb`.

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | _To be added after Tableau Public publishing_ |
| **Executive View** | KPI scorecard (Revenue, AOV, CSAT, On-Time %), monthly trend lines, top/bottom performing states |
| **Operational View** | Drill-down by state → category → seller; delivery delay heatmap; review score vs delivery time scatter; payment type breakdown |
| **Main Filters** | Date range, Customer State, Product Category, Payment Type, Review Score Band |

Store dashboard screenshots in [`tableau/screenshots/`](tableau/screenshots/) and document the public links in [`tableau/dashboard_links.md`](tableau/dashboard_links.md).

---

## Key Insights

_List 8-12 major findings from the analysis, written in decision language. Each insight should tell the reader what to think or act upon, not merely describe a chart._

1. _Insight 1_
2. _Insight 2_
3. _Insight 3_
4. _Insight 4_
5. _Insight 5_
6. _Insight 6_
7. _Insight 7_
8. _Insight 8_

---

## Recommendations

_Provide 3-5 specific, actionable business recommendations, each linked directly to an insight above._

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 2 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |
| 3 | _Which insight does this address?_ | _What should the stakeholder do?_ | _What measurable impact do you expect?_ |

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
|   |-- project_report_template.md
|   `-- presentation_outline.md
|
|-- docs/
|   `-- data_dictionary.md
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

The project follows a structured 7-step workflow:

1. **Define** - Sector selected, problem statement scoped, mentor approval obtained.
2. **Extract** - Raw dataset sourced and committed to `data/raw/`; data dictionary drafted.
3. **Clean and Transform** - Cleaning pipeline built in `notebooks/02_cleaning.ipynb` and optionally `scripts/etl_pipeline.py`.
4. **Analyze** - EDA and statistical analysis performed in notebooks `03` and `04`.
5. **Visualize** - Interactive Tableau dashboard built and published on Tableau Public.
6. **Recommend** - 3-5 data-backed business recommendations delivered.
7. **Report** - Final project report and presentation deck completed and exported to PDF in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, and KPI computation |
| Google Colab | Supported | Cloud notebook execution environment |
| Tableau Public | Mandatory | Dashboard design, publishing, and sharing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| SQL | Optional | Initial data extraction only, if documented |

**Recommended Python libraries:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`

---

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Is the business question clear and well-scoped? |
| Data Quality and ETL | 15 | Is the cleaning pipeline thorough and documented? |
| Analysis Depth | 25 | Are statistical methods applied correctly with insight? |
| Dashboard and Visualization | 20 | Is the Tableau dashboard interactive and decision-relevant? |
| Business Recommendations | 20 | Are insights actionable and well-reasoned? |
| Storytelling and Clarity | 10 | Is the presentation professional and coherent? |
| **Total** | **100** | |

> Marks are awarded for analytical thinking and decision relevance, not chart quantity, visual decoration, or code length.

---

## Submission Checklist

**GitHub Repository**

- [ ] Public repository created with the correct naming convention (`SectionName_TeamID_ProjectName`)
- [ ] All notebooks committed in `.ipynb` format
- [ ] `data/raw/` contains the original, unedited dataset
- [ ] `data/processed/` contains the cleaned pipeline output
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains the Tableau Public URL
- [ ] `docs/data_dictionary.md` is complete
- [ ] `README.md` explains the project, dataset, and team
- [ ] All members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter included
- [ ] Dashboard directly addresses the business problem

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] Cover page, executive summary, sector context, problem statement
- [ ] Data description, cleaning methodology, KPI framework
- [ ] EDA with written insights, statistical analysis results
- [ ] Dashboard screenshots and explanation
- [ ] 8-12 key insights in decision language
- [ ] 3-5 actionable recommendations with impact estimates
- [ ] Contribution matrix matches GitHub history

**Presentation Deck**

- [ ] Final presentation exported as PDF into `reports/`
- [ ] Title slide through recommendations, impact, limitations, and next steps

**Individual Assets**

- [ ] DVA-oriented resume updated to include this capstone
- [ ] Portfolio link or project case study added

---

## Contribution Matrix

This table must match evidence in GitHub Insights, PR history, and committed files.

| Team Member | Dataset and Sourcing | ETL and Cleaning | EDA and Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT and Viva |
|---|---|---|---|---|---|---|---|
| _Member 1_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 2_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 3_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 4_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 5_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |
| _Member 6_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ | _Owner / support_ |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** _____________________________

**Date:** _______________

---

## Academic Integrity

All analysis, code, and recommendations in this repository must be the original work of the team listed above. Free-riding is tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology - Data Visualization & Analytics | Capstone 2*
