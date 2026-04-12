import pytest
from algorithms.priority import priority_non_preemptive


class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        # các giá trị sẽ được tính
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


def test_tie_break_priority():
    processes = load_test_data()

    result_order, result_processes = priority_non_preemptive(processes)

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

    #TEST 1: đúng thứ tự execution
    assert result_order == expected_order, \
        f"Sai thứ tự! Expected {expected_order} nhưng ra {result_order}"


def test_all_process_completed():
    processes = load_test_data()

    _, result_processes = priority_non_preemptive(processes)

    #TEST 2: tất cả process phải được xử lý
    for p in result_processes:
        assert p.completion_time > 0, f"{p.pid} chưa được xử lý"


def test_waiting_time_non_negative():
    processes = load_test_data()

    _, result_processes = priority_non_preemptive(processes)

    #TEST 3: waiting time không âm
    for p in result_processes:
        assert p.waiting_time >= 0, f"{p.pid} có waiting_time âm"


def test_turnaround_time_correct():
    processes = load_test_data()

    _, result_processes = priority_non_preemptive(processes)

    #TEST 4: turnaround = completion - arrival
    for p in result_processes:
        assert p.turnaround_time == p.completion_time - p.arrival_time, \
            f"{p.pid} tính turnaround sai"