import sys

current_PU = None
distance_sum = 0
num_course = 0

for line in sys.stdin:
    Pu, distance = line.strip().split("\t")
    Pu = int(Pu)
    distance = float(distance)
    if Pu == current_PU:
        num_course += 1
        distance_sum += distance
    else:
        if current_PU is not None:
            distance_avg = distance_sum/num_course
            print(f"{Pu}\t{distance_avg}\t{num_course}")

            #current_PU = Pu
            distance_sum = 0
            num_course = 0

        current_PU = Pu
        num_course += 1
        distance_sum += distance

if current_PU is not None:
    print(f"{current_PU}\t{distance_avg}\t{num_course}")
