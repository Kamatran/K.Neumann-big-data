import sys

header = sys.stdin.readline().strip().split(",")
pu_idx = header.index("PULocationID")
dist_idx = header.index("trip_distance")

for line in sys.stdin:
    words = line.strip().split(",")
    trip_distance = words[dist_idx]
    PULocationID = words[pu_idx]
    print(f"{PULocationID}\t{trip_distance}")