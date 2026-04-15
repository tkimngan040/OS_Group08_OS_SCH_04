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

        if idx == -1:
            current_time = min(
                p.arrival_time for i, p in enumerate(processes) if not visited[i]
            )
            continue

        p = processes[idx]

        current_time += p.burst_time

        visited[idx] = True
        completed += 1
        order.append(p.pid)

    return order


# ======================
# TEST 1: NORMAL
# ======================
def test_sjf_normal():
    processes = read_csv("../input/test_sjf.csv")
    order = sjf_non_preemptive(processes)

    expected = ['P1', 'P3', 'P2', 'P12', 'P7', 'P13',
            'P5', 'P10', 'P8', 'P6', 'P4', 'P11', 'P9']

    assert order == expected, f"FAIL: {order} != {expected}"
    print("test_sjf_normal passed")


# ======================
# TEST 2: TIE-BREAKte
# ======================
def test_sjf_tie_break():
    processes = read_csv("../input/test_tie_break(SJF).csv")
    order = sjf_non_preemptive(processes)

    expected = [f"P{i}" for i in range(1, 18)]
    assert order == expected, f"FAIL: {order} != {expected}"
    print("test_sjf_tie_break passed")


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    test_sjf_normal()
    test_sjf_tie_break()

    print("All tests passed")