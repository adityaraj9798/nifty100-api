import pandas as pd
from sqlalchemy import create_engine

# 1. Paste your Render EXTERNAL URL right here inside the quotes:
CLOUD_DB_URL = "postgresql://nifty100_db_17pd_user:xE5ePLtqvKHuFXdbcwUWm5ZA30yTsG8A@dpg-d82bt5t0lvsc73c87jcg-a.singapore-postgres.render.com/nifty100_db_17pd"

print("Connecting to Render Cloud...")
engine = create_engine(CLOUD_DB_URL)

print("Uploading data...")

# 2. Read from the separate files inside your data/raw folder!
try:
    df_profile = pd.read_excel("data/raw/companies.xlsx") 
    df_profile.to_sql("api_dimcompany", engine, if_exists="append", index=False)
    print("✅ Profiles uploaded!")

    df_pl = pd.read_excel("data/raw/profitandloss.xlsx")
    df_pl.to_sql("api_factprofitloss", engine, if_exists="append", index=False)
    print("✅ Profit & Loss uploaded!")

    df_bs = pd.read_excel("data/raw/balancesheet.xlsx")
    df_bs.to_sql("api_factbalancesheet", engine, if_exists="append", index=False)
    print("✅ Balance Sheets uploaded!")

    print(" ALL DONE! Your live website is ready.")

except FileNotFoundError as e:
    print(f"\n❌ ERROR: Could not find the file {e.filename}. Check your folder paths!")