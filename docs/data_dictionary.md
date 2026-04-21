# Data Dictionary — Olist Brazilian E-Commerce Dataset

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | Brazilian E-Commerce Public Dataset by Olist |
| Source | Kaggle — https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| Raw files | 9 CSV files in `data/raw/` |
| Granularity | One row per order-item in the central table; related tables at order, customer, payment, review, product, seller, and geolocation grain |
| Time coverage | September 2016 – October 2018 |
| Total orders | ~99,441 |
| Total order items | ~112,650 |
| Language note | Product categories are in Portuguese; `product_category_name_translation.csv` maps them to English |

## Entity Relationship Overview

```
customers ──(customer_id)──► orders ──(order_id)──► order_items ──(product_id)──► products
                                  │                       │
                                  │                       └──(seller_id)──► sellers
                                  │
                                  ├──(order_id)──► order_payments
                                  └──(order_id)──► order_reviews

geolocation ──(zip_code_prefix)──► customers / sellers
product_category_name_translation ──(product_category_name)──► products
```

---

## Table 1: olist_orders_dataset.csv

**Grain**: One row per order. ~99,441 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `order_id` | string (hash) | Unique order identifier — primary key for this table | `e481f51cbdc54678b7cc49136f2d6af7` | Join key, KPIs | Some values quoted, some not — normalise quotes |
| `customer_id` | string (hash) | Links to `customers` table — one-to-one with orders | `9ef432eb6251297304e76186b10a928d` | Join key | |
| `order_status` | string | Current status of the order | `delivered`, `shipped`, `canceled`, `unavailable`, `processing`, `created`, `approved` | Filter, EDA | Only `delivered` orders should be used for satisfaction analysis; other statuses are edge cases |
| `order_purchase_timestamp` | datetime | When the customer placed the order | `2017-10-02 10:56:33` | Time-series, KPIs, seasonality | Parse as datetime; extract year/month/weekday/hour |
| `order_approved_at` | datetime | When the payment was approved | `2017-10-02 11:07:15` | Approval lag analysis | Contains nulls for canceled/unapproved orders |
| `order_delivered_carrier_date` | datetime | When the order was handed to the logistics carrier | `2017-10-04 19:55:00` | Carrier handoff analysis | Null for non-delivered orders |
| `order_delivered_customer_date` | datetime | When the customer received the order | `2017-10-10 21:25:13` | Delivery delay calculation | Null for ~3% of orders (non-delivered) |
| `order_estimated_delivery_date` | datetime | Estimated delivery date shown to customer at purchase | `2017-10-18 00:00:00` | On-time delivery KPI | Time component always `00:00:00` — date-only precision |

**Derived columns planned**:
- `delivery_delay_days` = `order_delivered_customer_date` − `order_estimated_delivery_date` (negative = early)
- `approval_lag_hours` = `order_approved_at` − `order_purchase_timestamp`
- `is_on_time` = `delivery_delay_days` ≤ 0
- `purchase_month`, `purchase_weekday`, `purchase_hour` — extracted from `order_purchase_timestamp`

---

## Table 2: olist_order_items_dataset.csv

**Grain**: One row per item within an order. An order can have multiple items. ~112,650 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `order_id` | string (hash) | Links to `orders` table | `00010242fe8c5a6d1ba2dd792cb16214` | Join key | |
| `order_item_id` | int | Sequential item number within the order (1-based) | `1`, `2`, `3` | Line-item count | Max value per order = number of items in that order |
| `product_id` | string (hash) | Links to `products` table | `4244733e06e7ecb4970a6e2683c13e61` | Join key | |
| `seller_id` | string (hash) | Links to `sellers` table | `48436dade18ac8b2bce089ec2a041202` | Join key, seller analysis | |
| `shipping_limit_date` | datetime | Deadline for seller to hand over to carrier | `2017-09-19 09:45:35` | Seller performance | Parse as datetime |
| `price` | float | Item price in Brazilian Reais (BRL) | `58.90` | Revenue, AOV, price analysis | Check for zero/negative values |
| `freight_value` | float | Shipping cost for this item in BRL | `13.29` | Freight analysis, freight-to-price ratio | Check for zero values (digital products?) |

**Derived columns planned**:
- `total_item_value` = `price` + `freight_value`
- `freight_ratio` = `freight_value` / `price` (handle division by zero)

---

## Table 3: olist_customers_dataset.csv

**Grain**: One row per order-customer mapping. ~99,441 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `customer_id` | string (hash) | Links to `orders` table — unique per order (not per person) | `06b8999e2fba1a1fbc88172c00ba8bc7` | Join key | |
| `customer_unique_id` | string (hash) | Identifies the same actual person across multiple orders | `861eff4711a542e4b93843c6dd7febb0` | Repeat purchase analysis | This is the true customer identifier — `customer_id` resets per order |
| `customer_zip_code_prefix` | string | First 5 digits of customer zip code | `14409` | Join to `geolocation`, geographic analysis | Stored as string to preserve leading zeros; numeric in raw file — cast to string |
| `customer_city` | string | Customer's city name (lowercase, Portuguese) | `franca`, `sao paulo` | Geographic analysis | Normalise casing; some cities may have accent characters |
| `customer_state` | string | Brazilian state abbreviation (2 letters) | `SP`, `RJ`, `MG` | Filters, geographic segmentation | 27 states + DF; verify all are valid Brazilian state codes |

**Important**: `customer_id` ≠ `customer_unique_id`. A returning customer gets a new `customer_id` per order but keeps the same `customer_unique_id`. Use `customer_unique_id` for repeat purchase and loyalty analysis.

---

## Table 4: olist_order_payments_dataset.csv

**Grain**: One row per payment attempt. An order can have multiple payments (sequential). ~103,886 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `order_id` | string (hash) | Links to `orders` table | `b81ef226f3fe1789b1e8b2acac839d17` | Join key | |
| `payment_sequential` | int | Payment sequence number within the order | `1`, `2`, `3` | Identify split payments | Sequential = 1 means single payment; >1 means customer used multiple methods |
| `payment_type` | string | Payment method used | `credit_card`, `boleto`, `voucher`, `debit_card`, `not_defined` | Payment analysis, filters | `not_defined` appears rarely — may need to be treated as null/unknown |
| `payment_installments` | int | Number of instalments for credit card payments | `8`, `1` | Instalment behaviour | = 1 means full payment; max can go high; boleto/voucher typically = 1 |
| `payment_value` | float | Transaction amount in BRL | `99.33` | Revenue KPIs, AOV | When aggregating per order, SUM all sequential payments |

**Aggregation note**: To get total order payment, group by `order_id` and SUM `payment_value`. To get primary payment type, take the type with `payment_sequential = 1`.

---

## Table 5: olist_order_reviews_dataset.csv

**Grain**: One row per review. Each order has at most one review. ~104,720 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `review_id` | string (hash) | Unique review identifier | `7bc2406110b926393aa56f80a40eba40` | Primary key | |
| `order_id` | string (hash) | Links to `orders` table | `73fc7af87114b39712e6da79b0a377eb` | Join key | Some orders may have duplicate reviews — check and keep latest |
| `review_score` | int | Customer satisfaction score (1 = worst, 5 = best) | `4`, `5`, `1` | CSAT KPI, target variable for analysis | Integer 1-5; no fractional scores |
| `review_comment_title` | string | Review title (optional) | _null in most rows_ | NLP (optional) | Highly sparse — majority null |
| `review_comment_message` | string | Review body text (optional, in Portuguese) | `Recebi bem antes do prazo estipulado.` | NLP (optional) | Highly sparse — ~58% null; text is Portuguese |
| `review_creation_date` | datetime | When the satisfaction survey was sent | `2018-01-18 00:00:00` | Review timing analysis | Date-only precision |
| `review_answer_timestamp` | datetime | When the customer answered the survey | `2018-01-18 21:46:59` | Response time analysis | Full datetime |

**Quality note**: `review_comment_title` and `review_comment_message` are mostly null. Use `review_score` as the primary satisfaction metric. Comment text can be used for optional qualitative analysis.

---

## Table 6: olist_products_dataset.csv

**Grain**: One row per product. ~32,951 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `product_id` | string (hash) | Unique product identifier | `1e9e8ef04dbcff4541ed26657ea517e5` | Join key | |
| `product_category_name` | string | Category name in Portuguese | `perfumaria`, `artes`, `esporte_lazer` | Category analysis | Join to translation table for English; ~2% null — these products have no category assigned |
| `product_name_lenght` | float | Number of characters in product name | `40`, `44` | Content quality analysis | Note: column name has typo "lenght" instead of "length"; has some nulls |
| `product_description_lenght` | float | Number of characters in product description | `287`, `276` | Content quality analysis | Typo in column name; has nulls |
| `product_photos_qty` | float | Number of product photos published | `1`, `2` | Listing quality analysis | Has nulls |
| `product_weight_g` | float | Product weight in grams | `225`, `1000` | Logistics analysis, freight estimation | Has nulls; possible outliers (very heavy items) |
| `product_length_cm` | float | Product length in centimetres | `16`, `30` | Logistics, volume calculation | Has nulls |
| `product_height_cm` | float | Product height in centimetres | `10`, `18` | Logistics, volume calculation | Has nulls |
| `product_width_cm` | float | Product width in centimetres | `14`, `20` | Logistics, volume calculation | Has nulls |

**Derived columns planned**:
- `product_volume_cm3` = `length` × `height` × `width`
- Join `product_category_name` → `product_category_name_english` via translation table

**Quality note**: Column names have typo "lenght". Several columns have nulls (~2% of rows). Products with null category may need an "uncategorised" label.

---

## Table 7: olist_sellers_dataset.csv

**Grain**: One row per seller. ~3,096 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `seller_id` | string (hash) | Unique seller identifier | `3442f8959a84dea7ee197c632cb2df15` | Join key, seller analysis | |
| `seller_zip_code_prefix` | string | First 5 digits of seller zip code | `13023` | Join to `geolocation`, logistics analysis | Cast to string to match geolocation table |
| `seller_city` | string | Seller's city name (lowercase, Portuguese) | `campinas`, `sao paulo` | Geographic analysis | Normalise casing |
| `seller_state` | string | Brazilian state abbreviation | `SP`, `RJ` | Seller geographic distribution | |

**Analysis opportunity**: Compute seller-level metrics — number of orders, avg review score, on-time shipping rate, total revenue — to identify top and bottom performers.

---

## Table 8: olist_geolocation_dataset.csv

**Grain**: One row per zip code prefix + lat/lng pair. Multiple entries per zip code. ~1,000,163 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `geolocation_zip_code_prefix` | string | First 5 digits of zip code | `01037` | Join key to customers/sellers | Numeric in raw file — cast to string |
| `geolocation_lat` | float | Latitude coordinate | `-23.545621` | Maps, geographic visualisation | Some outliers may be outside Brazil — validate range |
| `geolocation_lng` | float | Longitude coordinate | `-46.639292` | Maps, geographic visualisation | Validate range (Brazil: roughly -73 to -35 lng) |
| `geolocation_city` | string | City name | `sao paulo` | Geographic analysis | Inconsistent spelling/accents possible; city names vary across rows for same zip |
| `geolocation_state` | string | Brazilian state abbreviation | `SP` | Geographic analysis | |

**Critical aggregation note**: This table has ~1M rows with multiple lat/lng per zip code. Must aggregate by `geolocation_zip_code_prefix` (e.g., mean lat/lng, mode city/state) before joining to customers or sellers. Do NOT join raw — it will explode row count.

---

## Table 9: product_category_name_translation.csv

**Grain**: One row per product category. 71 rows.

| Column | Data Type | Description | Example | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `product_category_name` | string | Category name in Portuguese (foreign key to `products` table) | `beleza_saude` | Join key | |
| `product_category_name_english` | string | Category name in English | `health_beauty` | Category analysis, dashboard labels | Some English names have typos (e.g., `costruction_tools_garden`, `fashio_female_clothing`) — fix in cleaning |

**Quality note**: Some product categories in the `products` table may not have a matching row here. Handle with left join and fill missing as "uncategorised".

---

## Data Quality Summary

| Issue | Affected Tables | Severity | Handling Strategy |
|---|---|---|---|
| Null timestamps (delivered/approved dates) | `orders` | Medium | Filter to `order_status = 'delivered'` for time-based analysis; exclude nulls from delay calculations |
| Sparse review comments | `reviews` | Low | Use `review_score` only; ignore comment text unless doing optional NLP |
| Portuguese category names | `products` | Medium | Left join translation table; fill unmapped as "uncategorised" |
| Typos in English category names | `translation` | Low | Manual fix: `costruction` → `construction`, `fashio` → `fashion` |
| Typos in column names | `products` | Low | Rename `lenght` → `length` during cleaning |
| Geolocation 1M rows with duplicates per zip | `geolocation` | High | Aggregate by zip code prefix before joining (mean lat/lng, mode city/state) |
| Split payments (payment_sequential > 1) | `payments` | Medium | Aggregate to order level: SUM `payment_value`, take primary `payment_type` from sequential=1 |
| ~2% products with null category | `products` | Low | Label as "uncategorised" |
| Quoted vs unquoted values in CSV | `orders`, `items`, `customers` | Low | Standardise during load; pandas handles mixed quoting with default settings |
