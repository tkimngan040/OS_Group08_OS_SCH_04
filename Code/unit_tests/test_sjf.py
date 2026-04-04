import csv
from dataclasses import dataclass


# ======================
# Process class
# ======================
@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int = 0

    start_time: int = 0
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0


# ======================
# Read CSV
# ======================
def read_csv(file_name):
    processes = []
    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            processes.append(Process(
                pid=row['pid'],
                arrival_time=int(row['arrival_time']),
                burst_time=int(row['burst_time']),
                priority=int(row['priority'])
            ))
    return processes


# ======================
# SJF Non-preemptive
# ======================
def sjf_non_preemptive(processes):
    n = len(processes)

    current_time = 0
    completed = 0
    visited = [False] * n
    order = []

    processes = sorted(processes, key=lambda p: p.arrival_time)

    while completed < n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            p = processes[i]

            if not visited[i] and p.arrival_time <= current_time:

                if p.burst_time < min_bt:
                    min_bt = p.burst_time
                    idx = i

                elif p.burst_time == min_bt:
                    if p.arrival_time < processes[idx].arrival_time:
                        idx = i
                    elif p.arrival_time == processes[idx].arrival_time:
                        if int(p.pid[1:]) < int(processes[idx].pid[1:]):
                            idx = i

        # FIX idle CPU
        if idx == -1:
            current_time = min(
                p.arrival_time for i, p in enumerate(processes) if not visited[i]
            )
            continue

        p = processes[idx]

        p.start_time = current_time
        current_time += p.burst_time
        p.completion_time = current_time

        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        visited[idx] = True
        completed += 1
        order.append(p.pid)

    return order, processes


# ======================
# Print result
# ======================
def print_result(order, processes):
    print("Order:", " -> ".join(order))

    print("\nPID | AT | BT | ST | CT | TAT | WT")
    for p in processes:
        print(f"{p.pid:>3} | {p.arrival_time:>2} | {p.burst_time:>2} | "
              f"{p.start_time:>2} | {p.completion_time:>2} | "
              f"{p.turnaround_time:>3} | {p.waiting_time:>2}")

    avg_wt = sum(p.waiting_time for p in processes) / len(processes)
    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

    print("\nAverage WT:", round(avg_wt, 2))
    print("Average TAT:", round(avg_tat, 2))


# ======================
# MAIN TEST
# ======================
if __name__ == "__main__":

    print("========== TEST 1: NORMAL ==========")
    processes1 = read_csv("sjf_test.csv")
    order1, result1 = sjf_non_preemptive(processes1)
    print_result(order1, result1)

    print("\n\n========== TEST 2: TIE-BREAK ==========")
    processes2 = read_csv("test_tie_break_sjf.csv")
    order2, result2 = sjf_non_preemptive(processes2)
    print_result(order2, result2)