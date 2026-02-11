# E-Commerce Sales Analytics Platform

**End-to-end data analytics project analyzing 100,000+ Brazilian e-commerce orders**

![Project Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue)
![Tableau](https://img.shields.io/badge/Tableau-Public-orange)

---

## 📋 Table of Contents
- [Business Problem](#business-problem)
- [Solution Overview](#solution-overview)
- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Key Features](#key-features)
- [Data Schema](#data-schema)
- [Setup Instructions](#setup-instructions)
- [Analytics Queries](#analytics-queries)
- [Dashboards](#dashboards)
- [Key Insights](#key-insights)
- [Author](#author)

---

## 🎯 Business Problem

**Olist**, a Brazilian e-commerce marketplace, processes 100,000+ orders monthly across multiple product categories and sellers. The business teams needed a centralized analytics platform to:

- 📊 Monitor sales performance across regions and categories
- 👥 Identify high-value customers for retention campaigns
- 🏪 Track seller performance and delivery metrics
- 📈 Enable self-service analytics for data-driven decision making

**Pain Point:** Previously, analysts spent 2-3 days manually consolidating data from multiple CSV exports. This project automates the entire pipeline and provides real-time dashboards.

---

## 💡 Solution Overview

Built an **end-to-end Sales Analytics Platform** featuring:

1. **Automated ETL Pipeline** - Extracts data from 9 CSV sources, transforms into star schema, loads to PostgreSQL
2. **Data Warehouse** - Dimensional data model with 4 dimensions + 1 fact table (112,650 order line items)
3. **SQL Analytics** - 20+ business intelligence queries covering revenue, customers, products, and operations
4. **Interactive Dashboards** - Tableau visualizations for executive, product, and geographic analysis

---

## 🛠️ Tech Stack

**Languages & Libraries:**
- Python 3.9+ (pandas, SQLAlchemy, psycopg2)
- SQL (PostgreSQL 14+)

**Database:**
- PostgreSQL (dimensional data warehouse)

**Visualization:**
- Tableau Public

https://public.tableau.com/app/profile/arvind.iyer5945/viz/Dashboardformonthlytrendsforolistdata/Dashboard1?publish=yes

https://public.tableau.com/shared/BYXDFNT8T?:display_count=n&:origin=viz_share_link

**Tools:**
- Jupyter Notebooks (data exploration)
- Git & GitHub (version control)

---

## 🏗️ Project Architecture
```
┌─────────────────┐
│   Raw CSV Data  │  (9 files, 1M+ rows)
│   Olist Dataset │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ETL Pipeline   │  (Python - pandas)
│  • Extract      │
│  • Transform    │
│  • Load         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL DB  │  (Star Schema)
│  • 4 Dimensions │
│  • 1 Fact Table │
│  • 112K+ rows   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analytics Layer │
│  • 20+ Queries  │
│  • Exports      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Tableau Dashboards│
│  • Executive    │
│  • Product      │
│  • Geographic   │
└─────────────────┘
```

---

## ✨ Key Features

### 🔄 ETL Pipeline
- Processes 9 source CSV files (orders, customers, products, sellers, payments, reviews)
- Implements star schema with SCD Type 2 for historical tracking
- Automated data quality checks and validation
- Handles missing values, duplicates, and referential integrity

### 📊 Data Warehouse
- **Fact Table:** `fact_order_items` (112,650 rows) - Order line item grain
- **Dimensions:**
  - `dim_customers` (99,441 customers)
  - `dim_products` (32,951 products with English category translations)
  - `dim_sellers` (3,095 sellers)
  - `dim_date` (1,460 dates covering 2016-2019)

### 🔍 Analytics Capabilities
- Revenue trending and forecasting
- Customer segmentation and lifetime value
- Product category performance analysis
- Seller performance tracking
- Geographic market analysis
- Payment method preferences

---

## 📐 Data Schema

### Star Schema Design

**Fact Table: fact_order_items**
```
- order_item_key (PK)
- order_id, order_item_id
- customer_key (FK) → dim_customers
- product_key (FK) → dim_products
- seller_key (FK) → dim_sellers
- order_date_key (FK) → dim_date
- delivered_date_key (FK) → dim_date
- price, freight_value, total_item_value
- order_status, payment info, review_score
```

**Dimensions:**
- `dim_customers` - Customer demographics (city, state, zip)
- `dim_products` - Product catalog (category, weight, dimensions)
- `dim_sellers` - Seller information (location)
- `dim_date` - Date attributes (year, month, quarter, day of week)

**Why Star Schema?**
- Optimized for analytical queries
- Fast JOIN performance
- Easy to understand for business users
- Scalable to millions of rows

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Tableau Public (for dashboards)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ecommerce-analytics.git
cd ecommerce-analytics
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL database**
```sql
CREATE DATABASE ecommerce_analytics;
```

4. **Download Olist dataset**
- Download from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- Place CSV files in `data/raw/`

5. **Run ETL pipeline**
```bash
python etl/pandas/load.py
```

6. **Generate analytics exports**
```bash
python sql/run_analytics.py
```

---

## 📈 Analytics Queries

### Sample Queries Included:

**Revenue Analytics:**
- Monthly revenue trend
- Revenue by product category
- Revenue by customer state
- Average order value analysis

**Customer Analytics:**
- Customer acquisition by month
- Repeat customer rate
- Top customers by lifetime value
- Customer distribution by geography

**Product Analytics:**
- Best-selling products
- Category performance matrix
- Products with highest reviews
- Year-over-year category growth

**Operational Metrics:**
- Order status breakdown
- Payment method distribution
- Orders by day of week

*See `sql/analytics_queries.sql` for complete library of 20+ queries*

---

## 📊 Dashboards

### 1. Executive Summary Dashboard
- Monthly revenue trends
- Key performance indicators (KPIs)
- Top product categories
- Geographic revenue distribution

### 2. Product Performance Dashboard
- Category revenue breakdown
- Best-selling products
- Review score analysis
- Product metrics matrix

### 3. Geographic Analysis Dashboard
- Revenue by state (map visualization)
- Regional performance comparison
- State-level customer metrics

*Dashboard screenshots coming soon...*

---

## 💡 Key Insights

From analysis of 112,650 order line items:

📈 **Growth:** Revenue grew from R$ 143 (Sep 2016) to R$ 985K+ monthly (Aug 2018)

🏆 **Top Categories:** 
1. Health & Beauty
2. Watches & Gifts  
3. Bed, Bath & Table

🌍 **Geographic:** São Paulo (SP) accounts for 42% of customers

💳 **Payment:** Credit card is preferred method (76% of orders)

⭐ **Satisfaction:** 57% of reviews are 5-star ratings

---

## 📁 Project Structure
```
ecommerce-analytics/
├── data/
│   ├── raw/                    # Original CSV files
│   └── bronze/                 # (Future: PySpark layer)
├── etl/
│   └── pandas/
│       ├── extract.py          # Data extraction
│       ├── transform.py        # Star schema transformation
│       └── load.py             # PostgreSQL loading
├── sql/
│   ├── analytics_queries.sql   # Query library
│   ├── run_analytics.py        # Automation script
│   └── analytics_output/       # CSV exports for Tableau
├── notebooks/
│   └── 01_data_exploration.ipynb
├── dashboards/
│   └── screenshots/
├── README.md
└── requirements.txt
```

---

## 🎓 Skills Demonstrated

- **Data Engineering:** ETL pipeline design, data modeling, dimensional modeling
- **SQL:** Complex queries, window functions, CTEs, aggregations, joins
- **Python:** pandas, SQLAlchemy, data manipulation, automation
- **Data Visualization:** Tableau dashboard design, storytelling with data
- **Database Design:** Star schema, indexing, query optimization
- **Analytics:** Business metrics, KPIs, customer segmentation, cohort analysis

---

## 🔮 Future Enhancements

- [ ] Add PySpark implementation (Medallion architecture: Bronze/Silver/Gold)
- [ ] Implement customer RFM segmentation
- [ ] Build cohort retention analysis
- [ ] Add delivery time prediction model
- [ ] Create automated daily email reports
- [ ] Deploy dashboards to Tableau Server

---

## 👤 Author

**Arvind Mahesh Iyer**

- 🎓 B.Tech ECE, NIT Calicut (2025)
- 💼 Software Engineer @ J&J Global Sourcing
- 📧 arvind03iyer@gmail.com
- 🐙 [GitHub](https://github.com/ArvindIyer2003)

---

## 📄 License

This project uses the [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) available under CC BY-NC-SA 4.0 license.

---

## 🙏 Acknowledgments

- Olist for providing the public dataset
- Kaggle for hosting the data
- NIT Calicut for academic foundation

---

**⭐ If you found this project helpful, please star the repository!**
