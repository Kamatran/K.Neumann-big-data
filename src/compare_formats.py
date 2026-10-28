import pandas as pd

df_par = pd.read_parquet("/data/yellow_tripdata_2024-01.parquet").head(200000)
df_csv = pd.read_csv("/data/yellow_tripdata_2024-01.csv", nrows=200000)
print("\n" + "="*80)
print(f"{'Column':<25} | {'CSV Type':<15} | {'CSV Mem (bytes)':<18} | {'Parquet Type':<15} | {'Parquet Mem (bytes)'}")
print("="*80)

csv_mem = df_csv.memory_usage(deep=True)
parquet_mem = df_par.memory_usage(deep=True)

for col in df_csv.columns:
    csv_dtype = df_csv[col].dtype
    csv_bytes = csv_mem[col]
    
    parquet_dtype = df_par[col].dtype
    parquet_bytes = parquet_mem[col]
    
    print(f"{col:<25} | {str(csv_dtype):<15} | {csv_bytes:<18} | {str(parquet_dtype):<15} | {parquet_bytes}")

# Print totals
print("="*80)
print(f"{'TOTAL':<25} | {'':<15} | {csv_mem.sum():<18} | {'':<15} | {parquet_mem.sum()}")