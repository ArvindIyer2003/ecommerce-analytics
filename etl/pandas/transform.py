import pandas as pd
import numpy as np

from datetime import datetime

def transform_data(raw_data):
    """Transform raw data into star schema"""
    
    print("\n" + "=" * 70)
    print("TRANSFORMING DATA INTO STAR SCHEMA")
    print("=" * 70)
    
    # ====================================================================
    # DIMENSION 1: dim_customers
    # ====================================================================
    print("\n📊 Building dim_customers...")
    
    customers = raw_data['customers'].copy()
    
    # Clean and deduplicate
    dim_customers = customers.drop_duplicates(subset=['customer_id'])
    
    # Add surrogate key
    dim_customers['customer_key'] = range(1, len(dim_customers) + 1)
    
    # Add SCD Type 2 columns
    dim_customers['effective_start_date'] = pd.to_datetime('2016-01-01')
    dim_customers['effective_end_date'] = pd.to_datetime('2099-12-31')
    dim_customers['is_current'] = True
    
    # Reorder columns
    dim_customers = dim_customers[[
        'customer_key', 'customer_id', 'customer_unique_id',
        'customer_zip_code_prefix', 'customer_city', 'customer_state',
        'effective_start_date', 'effective_end_date', 'is_current'
    ]]
    
    print(f"   ✓ {len(dim_customers):,} customers")
    
    # ====================================================================
    # DIMENSION 2: dim_products (with category translation)
    # ====================================================================
    print("\n📦 Building dim_products...")
    
    products = raw_data['products'].copy()
    category_translation = raw_data['category_translation'].copy()
    
    # Handle missing categories
    products['product_category_name'] = products['product_category_name'].fillna('unknown')
    
    # Join with English translations
    dim_products = products.merge(
        category_translation,
        on='product_category_name',
        how='left'
    )
    
    # Fill missing English translations
    dim_products['product_category_name_english'] = dim_products['product_category_name_english'].fillna('unknown')
    
    # Clean numeric nulls
    numeric_cols = ['product_name_lenght', 'product_description_lenght', 
                    'product_photos_qty', 'product_weight_g', 
                    'product_length_cm', 'product_height_cm', 'product_width_cm']
    for col in numeric_cols:
        dim_products[col] = dim_products[col].fillna(0)
    
    # Deduplicate
    dim_products = dim_products.drop_duplicates(subset=['product_id'])
    
    # Add surrogate key
    dim_products['product_key'] = range(1, len(dim_products) + 1)
    
    # Add SCD Type 2 columns
    dim_products['effective_start_date'] = pd.to_datetime('2016-01-01')
    dim_products['effective_end_date'] = pd.to_datetime('2099-12-31')
    dim_products['is_current'] = True
    
    # Reorder columns
    dim_products = dim_products[[
        'product_key', 'product_id', 
        'product_category_name', 'product_category_name_english',
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm',
        'effective_start_date', 'effective_end_date', 'is_current'
    ]]
    
    print(f"   ✓ {len(dim_products):,} products")
    print(f"   ✓ {dim_products['product_category_name_english'].nunique()} unique categories")
    
    # ====================================================================
    # DIMENSION 3: dim_sellers
    # ====================================================================
    print("\n🏪 Building dim_sellers...")
    
    sellers = raw_data['sellers'].copy()
    
    # Deduplicate
    dim_sellers = sellers.drop_duplicates(subset=['seller_id'])
    
    # Add surrogate key
    dim_sellers['seller_key'] = range(1, len(dim_sellers) + 1)
    
    # Add SCD Type 2 columns
    dim_sellers['effective_start_date'] = pd.to_datetime('2016-01-01')
    dim_sellers['effective_end_date'] = pd.to_datetime('2099-12-31')
    dim_sellers['is_current'] = True
    
    # Reorder columns
    dim_sellers = dim_sellers[[
        'seller_key', 'seller_id',
        'seller_zip_code_prefix', 'seller_city', 'seller_state',
        'effective_start_date', 'effective_end_date', 'is_current'
    ]]
    
    print(f"   ✓ {len(dim_sellers):,} sellers")
    
    # ====================================================================
    # DIMENSION 4: dim_date
    # ====================================================================
    print("\n📅 Building dim_date...")
    
    orders = raw_data['orders'].copy()
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    
    # Get date range
    min_date = orders['order_purchase_timestamp'].min().date()
    max_date = orders['order_purchase_timestamp'].max().date()
    
    # Add buffer
    min_date = pd.to_datetime('2016-01-01').date()
    max_date = pd.to_datetime('2019-12-31').date()
    
    # Generate date range
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    
    dim_date = pd.DataFrame({
        'date_key': range(1, len(date_range) + 1),
        'full_date': date_range,
        'day': date_range.day,
        'month': date_range.month,
        'year': date_range.year,
        'quarter': date_range.quarter,
        'day_of_week': date_range.dayofweek,
        'day_name': date_range.day_name(),
        'month_name': date_range.month_name(),
        'is_weekend': date_range.dayofweek.isin([5, 6])
    })
    
    print(f"   ✓ {len(dim_date):,} dates ({min_date} to {max_date})")
    
    # ====================================================================
    # FACT TABLE: fact_order_items
    # ====================================================================
    print("\n💰 Building fact_order_items...")
    
    # Start with order_items
    order_items = raw_data['order_items'].copy()
    orders = raw_data['orders'].copy()
    payments = raw_data['payments'].copy()
    reviews = raw_data['reviews'].copy()
    
    # Convert dates
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_date'] = orders['order_purchase_timestamp'].dt.date
    orders['delivered_date'] = orders['order_delivered_customer_date'].dt.date
    
    # Aggregate payments by order
    print("   Aggregating payments...")
    payments_agg = payments.groupby('order_id').agg({
        'payment_value': 'sum',
        'payment_installments': 'sum',
        'payment_type': lambda x: x.value_counts().index[0]
    }).reset_index()
    
    payments_agg.columns = ['order_id', 'total_payment_value', 
                            'total_installments', 'primary_payment_type']
    
    # Aggregate reviews by order (just take the score)
    print("   Joining reviews...")
    reviews_agg = reviews[['order_id', 'review_score']].drop_duplicates(subset=['order_id'])
    
    # Build fact table
    print("   Joining all tables...")
    fact_order_items = order_items.copy()
    
    # Join orders
    fact_order_items = fact_order_items.merge(
        orders[['order_id', 'customer_id', 'order_status', 'order_date', 'delivered_date']], 
        on='order_id', 
        how='inner'
    )
    
    # Join payments
    fact_order_items = fact_order_items.merge(
        payments_agg, 
        on='order_id', 
        how='left'
    )
    
    # Join reviews
    fact_order_items = fact_order_items.merge(
        reviews_agg, 
        on='order_id', 
        how='left'
    )
    
    # Add foreign keys by joining with dimensions
    print("   Adding foreign keys...")
    
    # Customer key
    fact_order_items = fact_order_items.merge(
        dim_customers[['customer_id', 'customer_key']], 
        on='customer_id', 
        how='left'
    )
    
    # Product key
    fact_order_items = fact_order_items.merge(
        dim_products[['product_id', 'product_key']], 
        on='product_id', 
        how='left'
    )
    
    # Seller key
    fact_order_items = fact_order_items.merge(
        dim_sellers[['seller_id', 'seller_key']], 
        on='seller_id', 
        how='left'
    )
    
    # Order date key
    dim_date_merge = dim_date.copy()
    dim_date_merge['full_date'] = pd.to_datetime(dim_date_merge['full_date']).dt.date
    
    fact_order_items = fact_order_items.merge(
        dim_date_merge[['full_date', 'date_key']], 
        left_on='order_date', 
        right_on='full_date', 
        how='left'
    )
    fact_order_items = fact_order_items.rename(columns={'date_key': 'order_date_key'})
    fact_order_items = fact_order_items.drop(columns=['full_date'])
    
    # Delivered date key
    fact_order_items = fact_order_items.merge(
        dim_date_merge[['full_date', 'date_key']], 
        left_on='delivered_date', 
        right_on='full_date', 
        how='left'
    )
    fact_order_items = fact_order_items.rename(columns={'date_key': 'delivered_date_key'})
    fact_order_items = fact_order_items.drop(columns=['full_date'])
    
    # Calculate total item value
    fact_order_items['total_item_value'] = fact_order_items['price'] + fact_order_items['freight_value']
    
    # Add surrogate key
    fact_order_items['order_item_key'] = range(1, len(fact_order_items) + 1)
    
    # Select final columns
    fact_order_items = fact_order_items[[
        'order_item_key', 'order_id', 'order_item_id',
        'customer_key', 'product_key', 'seller_key', 
        'order_date_key', 'delivered_date_key',
        'order_status', 'price', 'freight_value', 'total_item_value',
        'total_payment_value', 'primary_payment_type', 'total_installments',
        'review_score'
    ]]
    
    # Remove rows with missing keys
    initial_count = len(fact_order_items)
    fact_order_items = fact_order_items.dropna(subset=['customer_key', 'product_key', 
                                                         'seller_key', 'order_date_key'])
    final_count = len(fact_order_items)
    
    print(f"   ✓ {final_count:,} order items")
    if initial_count != final_count:
        print(f"   ⚠️  Dropped {initial_count - final_count:,} rows with missing keys")
    
    # ====================================================================
    # SUMMARY
    # ====================================================================
    print("\n" + "=" * 70)
    print("✓ TRANSFORMATION COMPLETE")
    print("=" * 70)
    print(f"\n   Dimensions:")
    print(f"   - dim_customers: {len(dim_customers):,} rows")
    print(f"   - dim_products: {len(dim_products):,} rows")
    print(f"   - dim_sellers: {len(dim_sellers):,} rows")
    print(f"   - dim_date: {len(dim_date):,} rows")
    print(f"\n   Fact Table:")
    print(f"   - fact_order_items: {len(fact_order_items):,} rows")
    
    return {
        'dim_customers': dim_customers,
        'dim_products': dim_products,
        'dim_sellers': dim_sellers,
        'dim_date': dim_date,
        'fact_order_items': fact_order_items
    }

if __name__ == '__main__':
    from extract import extract_data
    raw_data = extract_data()
    transformed = transform_data(raw_data)
    print("\n✓ Transformation complete!")