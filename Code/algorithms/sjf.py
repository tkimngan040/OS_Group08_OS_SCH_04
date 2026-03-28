def sjf_non_preemptive(processes):
    n = len(processes)

    current_time = 0
    completed = 0
    visited = [False] * n
    order = []

    # (optional) sort theo arrival trước
    processes = sorted(processes, key=lambda p: p.arrival_time)

    while completed < n:
        idx = -1
        min_bt = float('inf')

        # tìm process phù hợp
        for i in range(n):
            p = processes[i]

            if not visited[i] and p.arrival_time <= current_time:

                # chọn BT nhỏ nhất
                if p.burst_time < min_bt:
                    min_bt = p.burst_time
                    idx = i

                # tie-break (fix lỗi idx = -1)
                elif p.burst_time == min_bt:
                    if idx == -1 or p.arrival_time < processes[idx].arrival_time:
                        idx = i

        # nếu chưa có process nào đến
        if idx == -1:
            current_time += 1
            continue

        p = processes[idx]

        # tính toán trực tiếp start, completion, turnaround, waiting
        p.start_time = current_time
        current_time += p.burst_time
        p.completion_time = current_time

        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        visited[idx] = True
        completed += 1
        order.append(p.pid)

    return order, processes
