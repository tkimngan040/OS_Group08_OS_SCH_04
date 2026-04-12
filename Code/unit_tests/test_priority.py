import pytest
from algorithms.priority import priority_non_preemptive


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.start_time = 0
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0


def load_test_data():
    return [
        Process("P1",0,5,2), Process("P2",0,5,2),
        Process("P3",1,4,2), Process("P4",1,4,2),
        Process("P5",2,6,2), Process("P6",2,6,2),
        Process("P7",3,3,2), Process("P8",3,3,2),
        Process("P9",4,5,2), Process("P10",4,5,2),
        Process("P11",5,2,2), Process("P12",5,2,2),
        Process("P13",6,4,2), Process("P14",6,4,2),
        Process("P15",7,1,2), Process("P16",7,1,2),
        Process("P17",8,3,2),
    ]


# =========================
# ✅ TEST 1: Thứ tự execution (QUAN TRỌNG NHẤT)
# =========================
def test_execution_order():
    processes = load_test_data()
    result_order, _ = priority_non_preemptive(processes)

    expected_order = [
        "P1","P2",
        "P3","P4",
        "P5","P6",
        "P7","P8",
        "P9","P10",
        "P11","P12",
        "P13","P14",
        "P15","P16",
        "P17"
    ]

    assert result_order == expected_order, \
        f"Sai thứ tự! Expected {expected_order}, nhưng ra {result_order}"


# =========================
# ✅ TEST 2: Công thức thời gian
# =========================
def test_time_calculation():
    processes = load_test_data()
    _, result = priority_non_preemptive(processes)

    for p in result:
        assert p.turnaround_time == p.completion_time - p.arrival_time
        assert p.waiting_time == p.turnaround_time - p.burst_time


# =========================
# ✅ TEST 3: Không chạy trước khi đến
# =========================
def test_start_time_valid():
    processes = load_test_data()
    _, result = priority_non_preemptive(processes)

    for p in result:
        assert p.start_time >= p.arrival_time, \
            f"{p.pid} chạy trước khi tới"


# =========================
# ✅ TEST 4: Tất cả process đều được chạy
# =========================
def test_all_completed():
    processes = load_test_data()
    _, result = priority_non_preemptive(processes)

    for p in result:
        assert p.completion_time > 0, \
            f"{p.pid} chưa được xử lý"


# =========================
# ✅ TEST 5: Input lỗi (burst_time <= 0)
# =========================
def test_invalid_burst_time():
    processes = [Process("P1", 0, 0, 2)]

    with pytest.raises(ValueError):
        priority_non_preemptive(processes)