import pandas as pd
import os
from utils.process import Process

def read_csv(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    df = pd.read_csv(file_path)

    required_cols = ['pid', 'arrival_time', 'burst_time']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Thiếu cột: {col}")

    processes = []
    for _, row in df.iterrows():
        if pd.isna(row['arrival_time']) or pd.isna(row['burst_time']):
            raise ValueError("Dữ liệu bị thiếu trong file CSV")

        priority = int(row['priority']) if 'priority' in df.columns else 0

        p = Process(
            str(row['pid']),
            int(row['arrival_time']),
            int(row['burst_time']),
            priority
        )
        processes.append(p)

    return processes
