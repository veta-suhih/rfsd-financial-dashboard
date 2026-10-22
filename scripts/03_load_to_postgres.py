"""
Загружает подготовленные CSV в PostgreSQL для подключения DataLens.
"""
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(DB_URL)

tables = {
    "dim_company": "dim_company.csv",
    "dim_industry": "dim_industry.csv",
    "dim_region": "dim_region.csv",
    "fact_financials": "fact_financials.csv",
}

for table, filename in tables.items():
    path = PROCESSED_DIR / filename
    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists="replace", index=False, chunksize=100_000)
    print(f"Загружено {len(df):,} строк в {table}")