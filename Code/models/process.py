import pandas as pd
import os

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        # Thông tin đầu vào từ file CSV
        self.pid = pid                # ID tiến trình (P1, P2...)
        self.arrival_time = arrival_time  # Thời điểm đến
        self.burst_time = burst_time      # Thời gian chạy thực tế
        self.priority = priority          # Độ ưu tiên

        # Các thông số tính toán (Thành viên khác sẽ dùng cái này)
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

    def __repr__(self):
        return f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time})"
