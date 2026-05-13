import pandas as pd
import numpy as np
import os

RAW_DIR = 'data/raw/'
CLEAN_DIR = 'data/clean/'
SECTOR_MAP_PATH = 'data/sector_mapping.csv'

# Ensure the clean directory exists
os.makedirs(CLEAN_DIR, exist_ok=True)

def standardize_columns(df):
    """Converts column names to lowercase with underscores (e.g., 'Equity Capital' -> 'equity_capital')"""
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('\n', '_')
    return df

def standardize_year(df):
    """Finds the year column and creates a clean integer 'fiscal_year' for the database."""
    # Look for a column that represents the time period
    year_col = next((col for col in df.columns if 'year' in col or 'period' in col), None)
    
    # If no obvious year column, assume it's the second column (index 1)
    if not year_col and len(df.columns) > 1:
        year_col = df.columns[1]
        
    if not year_col:
        return df
        
    def parse_year(y):
        y = str(y).strip().upper()
        if 'TTM' in y:
            return 2025  # Assuming Trailing Twelve Months is current year
        if '-' in y:     # e.g., Mar-24
            parts = y.split('-')
            if len(parts) > 1 and parts[1].isdigit():
                return int("20" + parts[1])
        if ' ' in y:     # e.g., Mar 2024
            parts = y.split(' ')
            if len(parts) > 1 and parts[1].isdigit():
                return int(parts[1])
        return 0

    df['fiscal_year'] = df[year_col].apply(parse_year)
    df.rename(columns={year_col: 'year_label'}, inplace=True)
    return df

def clean_companies():
    print("Processing companies.xlsx...")
    df = pd.read_excel(f"{RAW_DIR}companies.xlsx")
    df = standardize_columns(df)
    
    # Merge with your sector mappings if you created the file
    if os.path.exists(SECTOR_MAP_PATH):
        sectors = pd.read_csv(SECTOR_MAP_PATH)
        if 'symbol' in df.columns and 'symbol' in sectors.columns:
            df = pd.merge(df, sectors, on='symbol', how='left')
    
    df.to_csv(f"{CLEAN_DIR}dim_company.csv", index=False)

def process_financial_table(filename, table_type):
    print(f"Processing {filename}...")
    filepath = f"{RAW_DIR}{filename}"
    if not os.path.exists(filepath):
        print(f"  --> Warning: {filename} not found in {RAW_DIR}. Skipping.")
        return

    df = pd.read_excel(filepath)
    df = standardize_columns(df)
    df = standardize_year(df)
    
    # Convert all number strings to actual floats, replacing blanks with 0
    for col in df.columns:
        if col not in ['symbol', 'company_name', 'year_label', 'fiscal_year']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Specific Financial Math based on your project requirements
    if table_type == "pnl":
        try:
            df['net_profit_margin_pct'] = np.where(df['sales'] > 0, (df['net_profit'] / df['sales']) * 100, 0)
            df['expense_ratio_pct'] = np.where(df['sales'] > 0, (df['expenses'] / df['sales']) * 100, 0)
            df['interest_coverage'] = np.where(df['interest'] > 0, df['operating_profit'] / df['interest'], 0)
        except KeyError:
            print("  --> Note: P&L formulas skipped. Column names might differ slightly.")
        df.to_csv(f"{CLEAN_DIR}fact_profit_loss.csv", index=False)
        
    elif table_type == "bs":
        try:
            equity_total = df['equity_capital'] + df['reserves']
            df['debt_to_equity'] = np.where(equity_total > 0, df['borrowings'] / equity_total, 0)
        except KeyError:
            print("  --> Note: Balance Sheet formulas skipped. Column names might differ slightly.")
        df.to_csv(f"{CLEAN_DIR}fact_balance_sheet.csv", index=False)
        
    elif table_type == "cf":
        try:
            df['free_cash_flow'] = df['operating_activity'] + df['investing_activity']
        except KeyError:
            pass
        df.to_csv(f"{CLEAN_DIR}fact_cash_flow.csv", index=False)

if __name__ == "__main__":
    print("Starting Excel to Star Schema Transformation...")
    clean_companies()
    process_financial_table('profitandloss.xlsx', 'pnl')
    process_financial_table('balancesheet.xlsx', 'bs')
    process_financial_table('cashflow.xlsx', 'cf')
    print("Success! Check your data/clean/ folder.")