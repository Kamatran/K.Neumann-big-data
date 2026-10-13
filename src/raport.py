import pandas as pd
from pathlib import Path

CSV = Path("/dane/przejazdy.csv")
if not CSV.exists():
    raise SystemExit("Brak /dane/przejazdy.csv - uruchom najpierw generuj.py")

df = pd.read_csv(CSV)
print("wiersze:", len(df))
print("sredni dystans:", round(df["trip_distance"].mean(), 3))
print("sredni koszt:  ", round(df["fare_amount"].mean(), 3))
print("Zmiana")
