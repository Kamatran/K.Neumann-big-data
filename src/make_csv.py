# W2, Z0 - generates the CSV variant from the TLC Parquet file.
# Prints only what Z0 checks: memory use and column types are what Z2 measures.
import os
import pandas as pd

src = "/data/yellow_tripdata_2024-01.parquet"
dst = "/data/yellow_tripdata_2024-01.csv"

df = pd.read_parquet(src)
df.to_csv(dst, index=False)
print(f"rows            : {len(df):,}")
print(f"columns         : {len(df.columns)}")
print(f"parquet on disk : {os.path.getsize(src):,} bytes")
print(f"csv on disk     : {os.path.getsize(dst):,} bytes")
