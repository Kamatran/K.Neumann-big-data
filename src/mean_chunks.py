import pandas as pd
import numpy as np

df = pd.read_csv("data/yellow_tripdata_2024-01.csv", chunksize=1000000)

num = 1
mega_mean = []
distance_sum = 0
rows = 0
for chunk in df:
    local_mean = chunk["trip_distance"].mean()
    n = len(chunk)
    local_distance = chunk["trip_distance"].sum()
    local_median = chunk["trip_distance"].median()
    print(f"Chunk {num}")
    print("="*50)
    print(f"Number of rows: {n}")
    print(f"Distance mean: {local_mean}")
    print(f"Distance median: {local_median}")
    mega_mean.append(local_mean)
    distance_sum += local_distance
    rows += n
    num += 1
print("="*40)
print(f"Distance mean from whole file: {np.mean(mega_mean)}")
print(f"Distance mean from distance sum and rows: {distance_sum/rows}")
