def priority_non_preemptive(processes):
    """
    processes: list[Process]
    """

    n = len(processes)
    current_time = 0
    done = [False] * n
    completed = 0

    result_order = []

    while completed < n: #Thuật toán lặp cho đến khi tất cả tiến trình hoàn thành
        idx = -1

        for i in range(n):
            p = processes[i]

            # validate burst_time
            if p.burst_time <= 0:
                raise ValueError(f"Burst time không hợp lệ: {p.pid}")

            if not done[i] and p.arrival_time <= current_time: #xét các tiến trình đã đến/chưa thực hiện
                if idx == -1:
                    idx = i
                else:
                    current = processes[idx]

                    # so sánh priority
                    if p.priority < current.priority: #tiến trình có độ ưu tiên nhỏ hơn thì chọn trước
                        idx = i

                    # tie-break khi cùng priority
                    elif p.priority == current.priority:
                        # ưu tiên arrival_time nhỏ hơn
                        if p.arrival_time < current.arrival_time:
                            idx = i
                        # nếu arrival bằng → so pid (P1 < P2)
                        elif p.arrival_time == current.arrival_time:
                            if int(p.pid[1:]) < int(current.pid[1:]):
                                idx = i

        # chưa có tiến trình nào tới
        if idx == -1:
            current_time = min(
                p.arrival_time for i, p in enumerate(processes) if not done[i]
            )
            continue

        p = processes[idx]

        # tính toán
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.completion_time

        done[idx] = True
        completed += 1
        result_order.append(p.pid)

    return result_order, processes
