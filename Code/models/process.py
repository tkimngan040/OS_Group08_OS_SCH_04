import pandas as pd
import os

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        # Thông tin đầu vào từ file CSV
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # Các thông số tính toán
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time})"



def calculate_times(processes):

    processes.sort(key=lambda x: (x.arrival_time, int(x.pid[1:])))

    current_time = 0

    for p in processes:
        if p.burst_time <= 0:
            raise ValueError(f"Burst time không hợp lệ: {p.pid}")

        if current_time < p.arrival_time:
            current_time = p.arrival_time

        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.completion_time

    return processes
