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
    # Sắp xếp theo arrival time (FCFS)
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0

    for p in processes:
        
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # Thời điểm bắt đầu
        p.start_time = current_time

        # Thời điểm hoàn thành
        p.completion_time = p.start_time + p.burst_time

        # Turnaround time = CT - AT
        p.turnaround_time = p.completion_time - p.arrival_time

        # Waiting time = TAT - BT
        p.waiting_time = p.turnaround_time - p.burst_time

        # Cập nhật thời gian hiện tại
        current_time = p.completion_time

    return processes
