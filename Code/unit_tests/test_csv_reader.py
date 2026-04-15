import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from utils.csv_reader import read_csv


# ✅ Case 1
def test_read_csv_valid(tmp_path):
    print("\n[Case 1] Đọc file hợp lệ")

    file = tmp_path / "data.csv"
    df = pd.DataFrame({
        "pid": ["P1", "P2"],
        "arrival_time": [0, 1],
        "burst_time": [5, 3],
        "priority": [1, 2]
    })
    df.to_csv(file, index=False)

    processes = read_csv(file)

    print("→ Số process:", len(processes))
    print("→ Process đầu:", processes[0].pid, processes[0].arrival_time)

    assert len(processes) == 2


# ❌ Case 2
def test_read_csv_file_not_found():
    print("\n[Case 2] File không tồn tại")

    with pytest.raises(FileNotFoundError):
        read_csv("khong_ton_tai.csv")

    print("→ Đã bắt lỗi FileNotFoundError")


# ❌ Case 3
def test_read_csv_missing_column(tmp_path):
    print("\n[Case 3] Thiếu cột")

    file = tmp_path / "data.csv"
    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
    })
    df.to_csv(file, index=False)

    with pytest.raises((ValueError, KeyError)):
        read_csv(file)

    print("→ Đã bắt lỗi thiếu cột")


# ❌ Case 4
def test_read_csv_missing_value(tmp_path):
    print("\n[Case 4] Dữ liệu bị thiếu")

    file = tmp_path / "data.csv"
    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [None],
        "burst_time": [5]
    })
    df.to_csv(file, index=False)

    with pytest.raises((ValueError, TypeError)):
        read_csv(file)

    print("→ Đã bắt lỗi dữ liệu thiếu")


# ✅ Case 5
def test_read_csv_no_priority(tmp_path):
    print("\n[Case 5] Priority mặc định = 0")

    file = tmp_path / "data.csv"
    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
        "burst_time": [5],
        "priority": [None]
    })
    df.to_csv(file, index=False)

    processes = read_csv(file)

    print("→ Priority:", processes[0].priority)

    assert processes[0].priority == 0
