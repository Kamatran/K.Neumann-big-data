import sys
import pandas as pd

if len(sys.argv) > 1:
    n = int(sys.argv[1])
    print(f"Loading first {n} rows")
    df = pd.read_csv("/data/yellow_tripdata_2024-01.csv", nrows=n)
else:
    print("Lading entire file")
    df = pd.read_csv("/data/yellow_tripdata_2024-01.csv")

print(f"Number of rows: {len(df)}")

print(f"Memory usage: {df.memory_usage(deep=True).sum()} bytes, {df.memory_usage(deep=True).sum()/(1024**2)} MB")