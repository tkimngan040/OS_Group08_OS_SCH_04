from algorithms.priority import priority_non_preemptive
from Process import Process


def test_priority():
    processes = [
        Process("P1", 0, 5, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 8, 2),
        Process("P4", 3, 6, 2),
    ]

    order, result = priority_non_preemptive(processes)

    print("=== PRIORITY TEST (FINAL) ===")
    print("Thứ tự chạy:", order)

    print("\nChi tiết:")
    for p in result:
        print(
            f"{p.pid} | "
            f"AT={p.arrival_time} | "
            f"BT={p.burst_time} | "
            f"PR={p.priority} | "
            f"ST={p.start_time} | "
            f"CT={p.completion_time} | "
            f"WT={p.waiting_time} | "
            f"TAT={p.turnaround_time}"
        )

    # test tie-break (priority bằng nhau)
    assert order[0] == "P1" or order[0] == "P2"

    # test đủ process
    assert len(order) == 4


if __name__ == "__main__":
    test_priority()