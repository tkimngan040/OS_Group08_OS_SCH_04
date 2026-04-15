import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

import pytest
import pandas as pd
from utils.csv_reader import read_csv


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


def test_read_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv("khong_ton_tai.csv")


def test_read_csv_missing_column(tmp_path):
    file = tmp_path / "data.csv"

    df = pd.DataFrame({
        "pid": ["P1"],
        "arrival_time": [0],
    })
    df.to_csv(file, index=False)

    with pytest.raises((ValueError, KeyError)):
        read_csv(file)


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


#RUN BUTTON sẽ chạy pytest
if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])