# Presentation Deck — Olist Marketplace Analytics

*Export this content into 10-12 slides in Google Slides / PowerPoint / Canva. Each section = one slide.*

---

## Slide 1 — Title

**Olist Marketplace Analytics: Decoding the Drivers of Customer Satisfaction and Revenue**

- Sector: E-Commerce / Retail (Brazil)
- Team ID: _To be filled_
- Team Members: _Names_
- Faculty Mentor: _Name_
- Newton School of Technology | DVA Capstone 2

---

## Slide 2 — Context & Problem Statement

**The challenge**: Olist connects 3,000 sellers to customers across 27 Brazilian states, but not all transactions result in happy customers. Review scores span 1-5, delivery delays vary by region, and repeat purchase behaviour is unclear.

**Core question**: *Which operational levers — delivery speed, seller quality, product mix, pricing, or payment experience — most influence customer satisfaction and revenue?*

**Decision supported**: Enable Olist's VP of Marketplace Operations to allocate improvement budgets with data-backed evidence.

---

## Slide 3 — Data Engineering

| Metric | Value |
|---|---|
| Source | Olist Brazilian E-Commerce (Kaggle) |
| Tables | 9 relational CSVs |
| Orders | ~99,441 |
| Time range | Sep 2016 – Oct 2018 |
| Cleaning | 8 datetime columns parsed, 1M geolocation rows aggregated, payments consolidated, category translations fixed |
| Output | 110,197 rows × 48 columns |

**Join strategy**: Orders backbone → left join customers → items → products → sellers → payments (aggregated) → reviews (deduplicated)

---

## Slide 4 — KPI Framework

| KPI | Value |
|---|---|
| Total Revenue | BRL 15.3M |
| Avg Order Value | BRL 160.58 |
| On-Time Delivery | 93.4% |
| CSAT (Review Score) | 4.08 / 5 |
| Repeat Purchase Rate | 3.0% |
| Avg Delivery Delay | -11.2 days (early) |
| Platform Freight Ratio | 19.8% |

*Why these KPIs*: Each directly measures either customer satisfaction or revenue efficiency — the two business outcomes this project targets.

---

## Slide 5 — Key EDA Insights

1. **Revenue doubled** from Jan to Nov 2017 (Black Friday spike); non-seasonal months are weak
2. **SP alone = 40% of revenue** — geographic concentration risk
3. **Weekday 10am-4pm peak**; weekends drop 40% — schedule promotions for weekday afternoons
4. **High-revenue categories (furniture, computers) have below-average CSAT** — logistics quality fails for bulky items
5. **Review scores are bimodal** — love-it (5) or hate-it (1) — very little middle ground

*Include: Monthly revenue chart, state revenue bar, weekday-hour heatmap*

---

## Slide 6 — Statistical Analysis

| Test | Result | Key Finding |
|---|---|---|
| Welch's t-test (on-time vs late) | p < 0.001, Cohen's d > 0.8 | Late orders: 2.6/5 vs on-time: 4.2/5 |
| ANOVA (payment type vs AOV) | p < 0.001 | Credit card AOV BRL 170; voucher BRL 65 |
| Chi-squared (review × on-time) | Cramér's V ≈ 0.30 | Strong association between delivery and satisfaction |
| OLS Regression | is_late = largest negative coefficient | Meeting estimates > raw speed |
| RFM + K-Means (k=4) | 97% one-time buyers | Champions <5% of base but highest CLV |

**Overarching conclusion**: Delivery timeliness is the #1 operational lever. Payment and retention are secondary but complementary.

---

## Slide 7 — Dashboard Walkthrough

*Add screenshots from Tableau Public dashboard here.*

**Executive View**: KPI scorecard (Revenue, AOV, CSAT, On-Time %), monthly trend lines

**Operational View**: State → category → payment drill-downs; delivery delay heatmap; review vs delay scatter

**Filters**: Date range, Customer State, Product Category, Payment Type, Review Score Band

---

## Slide 8 — Top Insights (Decision Language)

1. **Late delivery is not a minor inconvenience — it's a satisfaction killer.** On-time: 4.2/5 → Late: 2.6/5. That's a 1.6-point drop on a 5-point scale.
2. **97% of customers never come back.** The platform is burning acquisition spend on one-time buyers.
3. **Meeting delivery estimates matters more than speed.** The binary "was it late?" shock outweighs incremental delivery days.
4. **Bulky categories are revenue engines with satisfaction leaks.** Furniture, computers, appliances generate high revenue but low reviews.
5. **Northern/Northeastern customers pay 2x freight for the same items.** This suppresses conversion in growth markets.

---

## Slide 9 — Recommendations

| # | What to Do | Expected Impact |
|---|---|---|
| 1 | **Set 95% on-time delivery targets** in carrier/seller SLAs. Focus on accurate estimation. | CSAT +0.3-0.5 pts; 10-15% fewer 1-star reviews |
| 2 | **Launch 7-day post-purchase nurture** (tracking, review prompt, recommendations). | +2-3pp repeat rate → 15-20% revenue lift |
| 3 | **Regional logistics partnerships** — forward warehouses in Manaus/Salvador. | 15-20% freight reduction in North/Northeast |
| 4 | **Premium logistics tier** for furniture/computers/appliances. | Protects BRL 2M+ from review-driven churn |
| 5 | **Zero-interest instalment partnerships** + boleto bundle offers. | +8-12% AOV in underserved payment segment |

---

## Slide 10 — Impact & Value

**Estimated combined impact if all 5 recommendations are implemented**:

- **CSAT improvement**: +0.3 to +0.5 points platform-wide
- **Revenue from retention**: +15-20% from repeat purchase uplift alone
- **Regional growth**: 15-20% freight reduction unlocks Northern/Northeastern markets
- **Category protection**: BRL 2M+ in furniture/computers/appliances revenue de-risked
- **AOV growth**: 8-12% increase in boleto and instalment segments

**Priority ranking**: On-time delivery SLA > Post-purchase nurture > Regional logistics > Premium category tier > Payment partnerships

---

## Slide 11 — Limitations

- Data covers 2016-2018 only; current operations may differ
- No customer demographics (age, gender, income) available
- Seller-side economics (margins, commissions) not included
- Causal inference limited — correlations ≠ causation
- Review text is sparse (~58% null) and in Portuguese

---

## Slide 12 — Next Steps

- **Predictive churn model** using gradient boosting for customer-level retention scoring
- **Seller performance index** — automated rating system tied to delivery and review metrics
- **A/B testing framework** — test delivery estimate accuracy vs customer satisfaction
- **NLP sentiment analysis** on Portuguese review text for qualitative satisfaction drivers
- **Real-time KPI dashboard** — move from static Tableau to live monitoring

**Tools don't get you marks. Thinking gets you marks.**
**Dashboards don't get you marks. Decisions get you marks.**
