import pandas as pd

df = pd.read_parquet("/data/yellow_tripdata_2024-01.parquet")
print(f"Number of rows: {len(df)}")
print(f"Mean trip distance: {df['trip_distance'].mean()}")
print(df.memory_usage(deep=True).sum())
