import pandas as pd
from sqlalchemy import create_engine
import os

# This URI matches the exact credentials we set in your docker-compose.yml
DB_URI = "postgresql://nifty_admin:supersecretpassword@localhost:5432/nifty100_warehouse"
CLEAN_DIR = 'data/clean/'

def load_to_postgres():
    print("Connecting to PostgreSQL Data Warehouse...")
    
    try:
        engine = create_engine(DB_URI)
        # Test the connection
        with engine.connect() as conn:
            pass
    except Exception as e:
        print(f"CRITICAL ERROR: Could not connect to the database. Is Docker running?\n{e}")
        return

    # Define tables to load (Dimension tables first, then Fact tables)
    tables_to_load = [
        ('dim_company', 'dim_company.csv'),
        ('fact_profit_loss', 'fact_profit_loss.csv'),
        ('fact_balance_sheet', 'fact_balance_sheet.csv'),
        ('fact_cash_flow', 'fact_cash_flow.csv')
    ]
    
    for table_name, file_name in tables_to_load:
        file_path = os.path.join(CLEAN_DIR, file_name)
        
        if not os.path.exists(file_path):
            print(f"  --> Warning: {file_name} not found in {CLEAN_DIR}. Skipping.")
            continue
            
        print(f"Loading {table_name}...")
        df = pd.read_csv(file_path)
        
        # Load the data! 
        # Using if_exists='replace' makes this script idempotent (safe to run multiple times)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"  -> Successfully loaded {len(df)} rows into {table_name}.")
        
    print("\n--- Data Warehouse Loading Complete! ---")

if __name__ == "__main__":
    load_to_postgres()