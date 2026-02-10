import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os

# Database config - UPDATE PASSWORD
DB_USER = 'postgres'
DB_PASSWORD = 'Seeth@15'  # UPDATE THIS
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ecommerce_analytics'

# Create output directory
os.makedirs('analytics_output', exist_ok=True)

# Connect
encoded_password = quote_plus(DB_PASSWORD)
engine = create_engine(f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

print("=" * 70)
print("RUNNING ANALYTICS QUERIES & EXPORTING TO CSV")
print("=" * 70)

queries = {
    'monthly_revenue': """
        SELECT 
            d.year, d.month, d.month_name,
            COUNT(DISTINCT f.order_id) as total_orders,
            ROUND(CAST(SUM(f.total_item_value) AS NUMERIC), 2) as total_revenue
        FROM fact_order_items f
        JOIN dim_date d ON f.order_date_key = d.date_key
        WHERE f.order_status = 'delivered'
        GROUP BY d.year, d.month, d.month_name
        ORDER BY d.year, d.month;
    """,
    
    'category_performance': """
        SELECT 
            p.product_category_name_english as category,
            COUNT(*) as units_sold,
            ROUND(CAST(SUM(f.total_item_value) AS NUMERIC), 2) as total_revenue,
            ROUND(CAST(AVG(f.review_score) AS NUMERIC), 2) as avg_review
        FROM fact_order_items f
        JOIN dim_products p ON f.product_key = p.product_key
        WHERE f.order_status = 'delivered'
        GROUP BY p.product_category_name_english
        ORDER BY total_revenue DESC;
    """,
    
    'state_performance': """
        SELECT 
            c.customer_state,
            COUNT(DISTINCT c.customer_key) as customers,
            COUNT(DISTINCT f.order_id) as orders,
            ROUND(CAST(SUM(f.total_item_value) AS NUMERIC), 2) as revenue
        FROM fact_order_items f
        JOIN dim_customers c ON f.customer_key = c.customer_key
        WHERE f.order_status = 'delivered'
        GROUP BY c.customer_state
        ORDER BY revenue DESC;
    """,
    
    'top_sellers': """
        SELECT 
            s.seller_id, s.seller_state,
            COUNT(DISTINCT f.order_id) as orders,
            ROUND(CAST(SUM(f.price) AS NUMERIC), 2) as revenue
        FROM fact_order_items f
        JOIN dim_sellers s ON f.seller_key = s.seller_key
        WHERE f.order_status = 'delivered'
        GROUP BY s.seller_id, s.seller_state
        ORDER BY revenue DESC
        LIMIT 50;
    """,
    
    'payment_methods': """
        SELECT 
            primary_payment_type,
            COUNT(DISTINCT order_id) as num_orders,
            ROUND(CAST(SUM(total_payment_value) AS NUMERIC), 2) as total_value
        FROM fact_order_items
        WHERE primary_payment_type IS NOT NULL
        AND order_status = 'delivered'
        GROUP BY primary_payment_type
        ORDER BY num_orders DESC;
    """
}

# Run each query and export
for name, query in queries.items():
    print(f"\n📊 Running: {name}")
    
    # Execute query and fetch results directly
    with engine.begin() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        
        # Create DataFrame from raw results
        df = pd.DataFrame(rows, columns=columns)
    
    # Save to CSV
    output_file = f'analytics_output/{name}.csv'
    df.to_csv(output_file, index=False)
    
    print(f"   ✓ {len(df)} rows")
    print(f"   ✓ Saved to {output_file}")
    print(df.head(10))

print("\n" + "=" * 70)
print("✓ ALL QUERIES COMPLETE - CSVs ready for Tableau!")
print("=" * 70)
print(f"\nCSV files saved in: sql/analytics_output/")
print("Next step: Load these CSVs into Tableau Public!")