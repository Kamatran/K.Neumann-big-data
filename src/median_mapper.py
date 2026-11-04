import sys

# Odczyt nagłówka
header = sys.stdin.readline().strip().split(",")
try:
    pu_idx = header.index("PULocationID")
    dist_idx = header.index("trip_distance")
except ValueError:
    sys.exit("Brak wymaganych kolumn")

for line in sys.stdin:
    parts = line.strip().split(",")
    if len(parts) > max(pu_idx, dist_idx):
        pu = parts[pu_idx].strip()
        dist = parts[dist_idx].strip()
        if pu and dist:
            print(f"{pu}\t{dist}\t1")
