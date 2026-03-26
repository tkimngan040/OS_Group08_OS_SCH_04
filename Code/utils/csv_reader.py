import pandas as pd
import os
from utils.process import Process

def read_csv(file_path):
    if not os.path.exists(file_path):
        print("Không tìm thấy file")
        return []

    df = pd.read_csv(file_path)

    processes = []
    for _, row in df.iterrows():
        p = Process(
            row['pid'],
            row['arrival_time'],
            row['burst_time'],
            row.get('priority', 0)
        )
        processes.append(p)

    return processes
