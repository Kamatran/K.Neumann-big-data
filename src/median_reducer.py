import sys

current_pu = None
zone_data = []  # Lista krotek: (dystans, licznik)

def process_zone(pu, data):
    if not data:
        return

    total_trips = sum(count for dist, count in data)
    unique_values = len(data)

    # Szukamy mediany
    # mid1 i mid2 obsługują zarówno parzystą, jak i nieparzystą liczbę elementów
    mid1 = (total_trips + 1) // 2
    mid2 = (total_trips + 2) // 2

    cum_count = 0
    val1 = 0.0
    val2 = 0.0
    found_mid1 = False

    for dist, count in data:
        cum_count += count
        if not found_mid1 and cum_count >= mid1:
            val1 = float(dist)
            found_mid1 = True
        if cum_count >= mid2:
            val2 = float(dist)
            break

    median_val = (val1 + val2) / 2.0
    print(f"{pu}\t{median_val:.3f}\t{total_trips}\t{unique_values}")

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    pu, dist, cnt_str = line.split("\t")
    cnt = int(cnt_str)

    if pu == current_pu:
        zone_data.append((float(dist), cnt))
    else:
        if current_pu is not None:
            process_zone(current_pu, zone_data)
        current_pu = pu
        zone_data = [(float(dist), cnt)]

if current_pu is not None:
    process_zone(current_pu, zone_data)
