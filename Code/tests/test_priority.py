from algorithms.priority import priority_non_preemptive
from Process import Process   # import class của team


def test_priority():
    # Tạo dữ liệu test
    processes = [
        Process("P1", 0, 5, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 8, 4),
        Process("P4", 3, 6, 2),
    ]

    order, result = priority_non_preemptive(processes)

    print("=== PRIORITY NON-PREEMPTIVE TEST ===")
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


if __name__ == "__main__":
    test_priority()