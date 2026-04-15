import pytest
import pandas as pd
from utils.csv_reader import read_csv


# ===================== CASE 1 =====================
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
    assert processes[1].arrival_time == 1


# ===================== CASE 2 =====================
def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv("khong_ton_tai.csv")


# ===================== CASE 3 =====================
def test_read_csv_missing_column(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
    })
    df.to_csv(file, index=False)

    with pytest.raises((ValueError, KeyError)):
        read_csv(file)


# ===================== CASE 4 =====================
def test_read_csv_missing_value(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [None],
        "burst_time": [5]
    })
    df.to_csv(file, index=False)

    with pytest.raises((ValueError, TypeError)):
        read_csv(file)


# ===================== CASE 5 =====================
def test_read_csv_no_priority(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
        "burst_time": [5],
        "priority": [None]
    })
    df.to_csv(file, index=False)

    processes = read_csv(file)

    assert processes[0].priority == 0