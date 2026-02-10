# Data Dictionary

## Fact Table

### fact_order_items
**Grain:** One row per order line item

| Column | Type | Description |
|--------|------|-------------|
| order_item_key | INTEGER | Primary key (surrogate) |
| order_id | TEXT | Business key - unique order identifier |
| order_item_id | INTEGER | Line item number within order |
| customer_key | INTEGER | Foreign key to dim_customers |
| product_key | INTEGER | Foreign key to dim_products |
| seller_key | INTEGER | Foreign key to dim_sellers |
| order_date_key | INTEGER | Foreign key to dim_date (order placed) |
| delivered_date_key | INTEGER | Foreign key to dim_date (delivered) |
| order_status | TEXT | delivered, shipped, canceled, etc. |
| price | DECIMAL | Product price |
| freight_value | DECIMAL | Shipping cost |
| total_item_value | DECIMAL | price + freight_value |
| total_payment_value | DECIMAL | Total payment for entire order |
| primary_payment_type | TEXT | credit_card, boleto, voucher, debit_card |
| total_installments | INTEGER | Number of payment installments |
| review_score | DECIMAL | Customer rating (1-5), NULL if no review |

---

## Dimension Tables

### dim_customers
**Grain:** One row per customer (SCD Type 2)

| Column | Type | Description |
|--------|------|-------------|
| customer_key | INTEGER | Primary key (surrogate) |
| customer_id | TEXT | Business key |
| customer_unique_id | TEXT | Unique customer identifier |
| customer_zip_code_prefix | TEXT | ZIP code (first 5 digits) |
| customer_city | TEXT | City name |
| customer_state | TEXT | Brazilian state (2-letter code) |
| effective_start_date | DATE | SCD Type 2 - valid from |
| effective_end_date | DATE | SCD Type 2 - valid to |
| is_current | BOOLEAN | SCD Type 2 - current record flag |

### dim_products
**Grain:** One row per product (SCD Type 2)

| Column | Type | Description |
|--------|------|-------------|
| product_key | INTEGER | Primary key (surrogate) |
| product_id | TEXT | Business key |
| product_category_name | TEXT | Category (Portuguese) |
| product_category_name_english | TEXT | Category (English translation) |
| product_name_lenght | INTEGER | Product name length in characters |
| product_description_lenght | INTEGER | Description length |
| product_photos_qty | INTEGER | Number of product photos |
| product_weight_g | DECIMAL | Weight in grams |
| product_length_cm | DECIMAL | Length in centimeters |
| product_height_cm | DECIMAL | Height in centimeters |
| product_width_cm | DECIMAL | Width in centimeters |
| effective_start_date | DATE | SCD Type 2 - valid from |
| effective_end_date | DATE | SCD Type 2 - valid to |
| is_current | BOOLEAN | SCD Type 2 - current record flag |

### dim_sellers
**Grain:** One row per seller (SCD Type 2)

| Column | Type | Description |
|--------|------|-------------|
| seller_key | INTEGER | Primary key (surrogate) |
| seller_id | TEXT | Business key |
| seller_zip_code_prefix | TEXT | ZIP code (first 5 digits) |
| seller_city | TEXT | City name |
| seller_state | TEXT | Brazilian state (2-letter code) |
| effective_start_date | DATE | SCD Type 2 - valid from |
| effective_end_date | DATE | SCD Type 2 - valid to |
| is_current | BOOLEAN | SCD Type 2 - current record flag |

### dim_date
**Grain:** One row per calendar date

| Column | Type | Description |
|--------|------|-------------|
| date_key | INTEGER | Primary key (surrogate) |
| full_date | DATE | Actual date |
| day | INTEGER | Day of month (1-31) |
| month | INTEGER | Month (1-12) |
| year | INTEGER | Year (2016-2019) |
| quarter | INTEGER | Quarter (1-4) |
| day_of_week | INTEGER | Day of week (0=Monday, 6=Sunday) |
| day_name | TEXT | Monday, Tuesday, etc. |
| month_name | TEXT | January, February, etc. |
| is_weekend | BOOLEAN | True if Saturday or Sunday |