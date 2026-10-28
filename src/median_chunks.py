import pandas as pd
import warnings
from collections import defaultdict

def main():
    warnings.simplefilter(action='ignore', category=pd.errors.DtypeWarning)

    csv_path = "/data/yellow_tripdata_2024-01.csv"
    chunksize = 1_000_000

    counts = defaultdict(int)

    for chunk in pd.read_csv(csv_path, chunksize=chunksize):

        for dist, count in chunk['trip_distance'].value_counts().items():
            counts[dist] += count

    sorted_items = sorted(counts.items())
    total_rows = sum(c for v, c in sorted_items)

    mid1 = (total_rows - 1) // 2
    mid2 = total_rows // 2

    current_pos = 0
    val1 = None
    val2 = None

    for v, c in sorted_items:
        if val1 is None and current_pos + c > mid1:
            val1 = v
        if val2 is None and current_pos + c > mid2:
            val2 = v
            break
        current_pos += c

    median = (val1 + val2) / 2.0

    print(f"Mediana: {median}")
    print(f"Liczba pozycji: {len(counts)}")

if __name__ == "__main__":
    main()
