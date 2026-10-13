# Generates a small, deterministic sample of trip records on the mounted volume.
import csv, random

random.seed(42)
with open("/dane/przejazdy.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["trip_distance", "fare_amount", "passenger_count"])
    for _ in range(1000):
        km = round(random.uniform(0.5, 25.0), 2)
        w.writerow([km, round(2.5 + km * 1.8, 2), random.randint(1, 4)])
print("zapisano /dane/przejazdy.csv")
