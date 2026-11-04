import pandas as pd
import os

# Ścieżki wewnątrz kontenera client
parquet_path = "/data/yellow_tripdata_2024-01.parquet"
if not os.path.exists(parquet_path):
    parquet_path = "/data/yellow_tripdata_2024-01.csv" # Fallback

mean_file = "/out/z1-mean.tsv"
median_file = "/out/z3-median.tsv"
z2_file = "/out/z2-avg.tsv" # Opcjonalnie, do sprawdzenia wariantu z błędnym combinerem

print(f"1. Wczytywanie danych źródłowych z: {parquet_path}")
if parquet_path.endswith('.parquet'):
    df = pd.read_parquet(parquet_path)
else:
    df = pd.read_csv(parquet_path)

# Obliczamy "prawdę" (ground truth) za pomocą Pandas
gt = df.groupby('PULocationID')['trip_distance'].agg(
    count='count',
    mean='mean',
    median='median'
).reset_index()
# Rzutuemy na string, aby dopasować do tekstowego sortowania Hadoopa (1, 10, 100...)
gt['PULocationID'] = gt['PULocationID'].astype(str)

print(f"   Znaleziono stref w danych źródłowych: {len(gt)}")

# --- SPRAWDZENIE ŚREDNIEJ (Z1) ---
if os.path.exists(mean_file):
    print("\n2. Weryfikacja średniej (z1-mean.tsv)")
    h_mean = pd.read_csv(mean_file, sep='\t', header=None, names=['PULocationID', 'h_mean', 'h_count'])
    h_mean['PULocationID'] = h_mean['PULocationID'].astype(str)

    merged = pd.merge(gt, h_mean, on='PULocationID', how='outer')
    merged['mean_diff'] = abs(merged['mean'] - merged['h_mean'])
    merged['count_match'] = merged['count'] == merged['h_count']

    print(f"   Stref w wyniku Hadoopa: {len(h_mean)}")
    print(f"   Czy liczba kursów się zgadza wszędzie? {merged['count_match'].all()}")
    print(f"   Największa różnica średnich: {merged['mean_diff'].max():.5f}")
else:
    print(f"\n[OSTRZEŻENIE] Brak pliku {mean_file}")

# --- SPRAWDZENIE MEDIANy (Z3) ---
if os.path.exists(median_file):
    print("\n3. Weryfikacja mediany (z3-median.tsv)")
    h_med = pd.read_csv(median_file, sep='\t', header=None, names=['PULocationID', 'h_median', 'h_count', 'h_unique'])
    h_med['PULocationID'] = h_med['PULocationID'].astype(str)

    merged_med = pd.merge(gt, h_med, on='PULocationID', how='outer')
    # Porównujemy z dokładnością do 3 miejsc po przecinku
    merged_med['med_diff'] = abs(merged_med['median'].round(3) - merged_med['h_median'].round(3))

    diff_count = (merged_med['med_diff'] > 0.001).sum()
    print(f"   Stref w wyniku Hadoopa: {len(h_med)}")
    print(f"   Liczba różnych median (różnica > 0.001): {diff_count}")

    print("\n   Wartości kontrolne dla wybranych stref:")
    for zone in ['1', '100', '132', '161', '237']:
        row = merged_med[merged_med['PULocationID'] == zone]
        if not row.empty:
            r = row.iloc[0]
            print(f"   Strefa {zone:3}: mediana={r['h_median']:.3f}, kursów={int(r['h_count']):6}, unikalnych={int(r['h_unique'])}")
else:
    print(f"\n[OSTRZEŻENIE] Brak pliku {median_file}")

# --- SPRAWDZENIE WARIANTU Z2-AVG (jeśli istnieje) ---
if os.path.exists(z2_file):
    print("\n4. Weryfikacja wariantu z2-avg (błędny combiner)")
    h_z2 = pd.read_csv(z2_file, sep='\t', header=None, names=['PULocationID', 'z2_mean', 'z2_count'])
    h_z2['PULocationID'] = h_z2['PULocationID'].astype(str)

    merged_z2 = pd.merge(gt, h_z2, on='PULocationID', how='inner')
    merged_z2['z2_diff'] = abs(merged_z2['mean'] - merged_z2['z2_mean'])

    bad_zones = merged_z2[merged_z2['z2_diff'] > 0.01]
    print(f"   Liczba stref różniących się o > 0.01: {len(bad_zones)}")

    if len(bad_zones) > 0:
        print("   10 największych różnic:")
        top_diff = bad_zones.nlargest(10, 'z2_diff')[['PULocationID', 'count', 'mean', 'z2_mean', 'z2_diff']]
        # Zmieniamy nazwy kolumn dla czytelności wydruku
        top_diff = top_diff.rename(columns={'count': 'kursy', 'mean': 'prawda_mean', 'z2_mean': 'z2_mean', 'z2_diff': 'roznica'})
        print(top_diff.to_string(index=False, float_format="%.4f"))
