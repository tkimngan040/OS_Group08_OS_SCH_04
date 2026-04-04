def generate_stress():
    import csv
    data = []
    burst_pattern = [5,8,3,10,2,6,4,7,1,9]
    priority_pattern = [3,5,1,4,2]

    arrival = 0

    for i in range(1, 1001):
        pid = f"P{i}"
        burst = burst_pattern[(i-1) % len(burst_pattern)]
        priority = priority_pattern[(i-1) % len(priority_pattern)]
        data.append([pid, arrival, burst, priority])
        arrival += 2 if i % 2 == 1 else 3

    with open("test_Stress.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pid", "arrival_time", "burst_time", "priority"])
        writer.writerows(data)


generate_stress()