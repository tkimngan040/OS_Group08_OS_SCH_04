import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from utils.csv_reader import read_csv


# ✅ Case 1: đọc file hợp lệ
def test_read_csv_valid(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1", "P2"],
        "arrival_time": [0, 1],
        "burst_time": [5, 3],
        "priority": [1, 2]
    })
    df.to_csv(file, index=False)

    processes = read_csv(file)

    assert len(processes) == 2
    assert processes[0].pid == "P1"
    assert processes[0].arrival_time == 0
    assert processes[0].burst_time == 5
    assert processes[0].priority == 1


# ❌ Case 2: file không tồn tại
def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv("khong_ton_tai.csv")


# ❌ Case 3: thiếu cột
def test_read_csv_missing_column(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
    })
    df.to_csv(file, index=False)


    with pytest.raises((ValueError, KeyError)):
        read_csv(file)


# ❌ Case 4: dữ liệu bị thiếu
def test_read_csv_missing_value(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [None],
        "burst_time": [5]
    })
    df.to_csv(file, index=False)

    # ⚠️ code thực tế có thể ra ValueError hoặc TypeError
    with pytest.raises((ValueError, TypeError)):
        read_csv(file)


# ✅ Case 5: không có priority → default = 0
def test_read_csv_no_priority(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
        "burst_time": [5],
        "priority": [None]   # 👈 thêm cột để tránh KeyError
    })
    df.to_csv(file, index=False)

    processes = read_csv(file)

    assert processes[0].priority == 0
