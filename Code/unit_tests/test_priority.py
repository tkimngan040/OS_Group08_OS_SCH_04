import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from algorithms.priority import priority_non_preemptive


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # sẽ được gán trong thuật toán
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None


# ===================== TEST CASES =====================

def test_basic_case():
    processes = [
        Process("P1", 0, 4, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 1, 3),
    ]

    order, result = priority_non_preemptive(processes)

    # thứ tự đúng theo priority
    assert order == ["P1", "P2", "P3"]

    # kiểm tra thời gian cụ thể
    assert result[0].completion_time == 4
    assert result[1].completion_time == 7
    assert result[2].completion_time == 8


def test_priority_order():
    processes = [
        Process("P1", 0, 5, 3),
        Process("P2", 0, 3, 1),
        Process("P3", 0, 2, 2),
    ]

    order, _ = priority_non_preemptive(processes)

    # priority nhỏ hơn chạy trước
    assert order == ["P2", "P3", "P1"]


def test_tie_break_arrival_time():
    processes = [
        Process("P1", 2, 3, 1),
        Process("P2", 1, 3, 1),
    ]

    order, _ = priority_non_preemptive(processes)

    # arrival_time nhỏ hơn chạy trước
    assert order == ["P2", "P1"]


def test_tie_break_pid():
    processes = [
        Process("P2", 0, 3, 1),
        Process("P1", 0, 3, 1),
    ]

    order, _ = priority_non_preemptive(processes)

    # cùng arrival + priority → pid nhỏ hơn trước
    assert order == ["P1", "P2"]


def test_idle_time():
    processes = [
        Process("P1", 5, 2, 1),
        Process("P2", 6, 1, 2),
    ]

    order, result = priority_non_preemptive(processes)

    # CPU phải nhảy thời gian đến 5
    assert result[0].start_time == 5
    assert order == ["P1", "P2"]


def test_invalid_burst_time():
    processes = [
        Process("P1", 0, 0, 1),
    ]

    with pytest.raises(ValueError):
        priority_non_preemptive(processes)


def test_waiting_time_calculation():
    processes = [
        Process("P1", 0, 4, 1),
        Process("P2", 1, 3, 2),
    ]

    _, result = priority_non_preemptive(processes)

    # P1 chạy trước → P2 phải đợi
    assert result[1].waiting_time == 3

    if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main([__file__]))