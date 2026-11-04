import sys

current_key = None
count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    pu, dist, cnt_str = line.split("\t")
    cnt = int(cnt_str)
    key = (pu, dist)

    if key == current_key:
        count += cnt
    else:
        if current_key is not None:
            print(f"{current_key[0]}\t{current_key[1]}\t{count}")
        current_key = key
        count = cnt

# Nie zapomnij o ostatnim kluczu
if current_key is not None:
    print(f"{current_key[0]}\t{current_key[1]}\t{count}")
