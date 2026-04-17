import csv
import os
from dataclasses import dataclass

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
                    if idx == -1 or p.arrival_time < processes[idx].arrival_time:
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

        current_time += p.burst_time

        visited[idx] = True
        completed += 1
        order.append(p.pid)

    return order


# ======================
# TEST 1: NORMAL
# ======================
def test_sjf_normal():
    file_path = os.path.join(BASE_DIR, "input", "test_sjf.csv")
    processes = read_csv(file_path)

    order = sjf_non_preemptive(processes)

    expected = ['P1', 'P3', 'P2', 'P12', 'P7', 'P13',
                'P5', 'P10', 'P8', 'P6', 'P4', 'P11', 'P9']

    assert order == expected


# ======================
# TEST 2: TIE-BREAK
# ======================
def test_sjf_tie_break():
    file_path = os.path.join(BASE_DIR, "input", "test_tie_break(SJF).csv")
    processes = read_csv(file_path)

    order = sjf_non_preemptive(processes)

    expected = [f"P{i}" for i in range(1, 18)]

    assert order == expected


# ======================
# RUN WITH PYTHON
# ======================
if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))