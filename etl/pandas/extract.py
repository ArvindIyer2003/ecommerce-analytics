import pandas as pd
import os

DATA_DIR = 'data/raw'

def extract_data():
    """Extract data from all 9 CSV files"""
    
    print("=" * 70)
    print("EXTRACTING DATA FROM CSV FILES")
    print("=" * 70)
    
    # Load all datasets
    datasets = {}
    
    files = {
        'orders': 'olist_orders_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'customers': 'olist_customers_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'payments': 'olist_order_payments_dataset.csv',
        'reviews': 'olist_order_reviews_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
        # Note: We're skipping geolocation (too messy, not needed)
    }
    
    for name, filename in files.items():
        filepath = os.path.join(DATA_DIR, filename)
        print(f"\nLoading {name}...")
        try:
            df = pd.read_csv(filepath)
            datasets[name] = df
            print(f"✓ {name}: {len(df):,} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            raise
    
    print("\n" + "=" * 70)
    print("✓ ALL DATA EXTRACTED SUCCESSFULLY")
    print("=" * 70)
    
    return datasets

if __name__ == '__main__':
    data = extract_data()
    print("\n📊 Sample from orders table:")
    print(data['orders'].head())