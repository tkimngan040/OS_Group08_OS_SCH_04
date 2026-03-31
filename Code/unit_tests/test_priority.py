import copy

from process import Process
from priority import priority_non_preemptive


# ================= DATA TEST =================
def create_test_data():
    return [
        Process("P1", 0, 5, 2),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 8, 4),
        Process("P4", 3, 6, 2),
    ]


# ================= GANTT =================
def show_gantt(processes, order):
    chart = ""
    timeline = ""

    process_map = {p.pid: p for p in processes}

    for pid in order:
        p = process_map[pid]
        chart += f"| {p.pid} "
        timeline += f"{p.start_time}    "

    chart += "|"
    last = process_map[order[-1]]
    timeline += str(last.completion_time)

    print("\nGantt Chart:")
    print(chart)
    print(timeline)


# ================= PRINT TABLE =================
def print_table(processes):
    print("\nChi tiết tiến trình:")

    print(f"{'PID':<5}{'AT':<5}{'BT':<5}{'PR':<5}{'ST':<5}{'CT':<5}{'WT':<5}{'TAT':<5}")

    # giống GUI → sort theo start_time
    processes = sorted(processes, key=lambda p: p.start_time)

    for p in processes:
        print(f"{p.pid:<5}{p.arrival_time:<5}{p.burst_time:<5}{p.priority:<5}"
              f"{p.start_time:<5}{p.completion_time:<5}{p.waiting_time:<5}{p.turnaround_time:<5}")


# ================= AVERAGE =================
def show_average(processes):
    avg_wt = sum(p.waiting_time for p in processes) / len(processes)
    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")


# ================= MAIN TEST =================
def main():
    processes = create_test_data()

    # giống GUI → tránh bug
    processes_copy = copy.deepcopy(processes)

    order, result = priority_non_preemptive(processes_copy)

    print("Execution Order:", " -> ".join(order))

    print_table(result)
    show_gantt(result, order)
    show_average(result)


if __name__ == "__main__":
    main()