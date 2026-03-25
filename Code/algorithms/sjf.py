def sjf_non_preemptive(processes):
    n = len(processes)
    
    current_time = 0
    completed = 0
    visited = [False] * n
    order = []  # lưu thứ tự chạy (Gantt)

    while completed < n:
        idx = -1
        min_bt = float('inf')

        # tìm process phù hợp
        for i in range(n):
            p = processes[i]
            if not visited[i] and p.arrival_time <= current_time:
                if p.burst_time < min_bt:
                    min_bt = p.burst_time
                    idx = i

                # tie-break: nếu BT bằng nhau → chọn arrival nhỏ hơn
                elif p.burst_time == min_bt:
                    if p.arrival_time < processes[idx].arrival_time:
                        idx = i

        # nếu chưa có process nào đến → CPU idle
        if idx == -1:
            current_time += 1
            continue

        p = processes[idx]

        # tính toán thời gian
        p.start_time = current_time
        current_time += p.burst_time
        p.completion_time = current_time

        # dùng hàm bạn đã nâng cấp
        p.calculate_times()

        visited[idx] = True
        completed += 1
        order.append(p.pid)

    return order, processes