import pandas as pd

df = pd.read_csv("/data/yellow_tripdata_2024-01.csv")
print(f"Number of rows: {len(df)}")
print(f"Mean trip distance: {df['trip_distance'].mean()}")