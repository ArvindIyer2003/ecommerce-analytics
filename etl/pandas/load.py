from sqlalchemy import create_engine,text
from urllib.parse import quote_plus
import pandas as pd

# Database configuration - UPDATE THESE
DB_USER = 'postgres'
DB_PASSWORD = 'Seeth@15'  # CHANGE THIS
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'ecommerce_analytics'

def load_to_postgres(data_dict):
    """Load transformed data to PostgreSQL"""
    
    print("\n" + "=" * 70)
    print("LOADING DATA TO POSTGRESQL")
    print("=" * 70)
    
    # Create connection
    encoded_password = quote_plus(DB_PASSWORD)
    connection_string = f'postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    engine = create_engine(connection_string)
    
    print(f"\n📡 Connecting to database: {DB_NAME}")
    
    # Load each table
    for table_name, df in data_dict.items():
        print(f"\n📥 Loading {table_name}...")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
        
        try:
            df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)
            print(f"   ✓ {table_name} loaded successfully")
        except Exception as e:
            print(f"   ✗ {table_name} failed: {e}")
            raise
    
    # Verify counts
    print("\n" + "=" * 70)
    print("VERIFYING DATA LOAD")
    print("=" * 70)
    
    with engine.connect() as conn:
        for table_name in data_dict.keys():
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.fetchone()[0]
            print(f"   {table_name}: {count:,} rows")
    
    print("\n" + "=" * 70)
    print("✓ ALL DATA LOADED TO POSTGRESQL")
    print("=" * 70)

if __name__ == '__main__':
    from extract import extract_data
    from transform import transform_data
    
    print("=" * 70)
    print("PANDAS ETL PIPELINE - FULL RUN")
    print("=" * 70)
    
    # Extract
    raw_data = extract_data()
    
    # Transform
    transformed_data = transform_data(raw_data)
    
    # Load
    load_to_postgres(transformed_data)
    
    print("\n" + "=" * 70)
    print("✓✓✓ ETL PIPELINE COMPLETE! ✓✓✓")
    print("=" * 70)