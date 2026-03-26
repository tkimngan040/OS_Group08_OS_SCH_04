def priority_non_preemptive(processes):
    """
    processes: list[Process]
    """

    n = len(processes)

    # Sắp xếp ban đầu theo arrival
    processes.sort(key=lambda x: x.arrival_time)

    current_time = 0
    done = [False] * n
    completed = 0

    result_order = []

    while completed < n:
        idx = -1
        best_priority = float('inf')

        # tìm process phù hợp
        for i in range(n):
            p = processes[i]

            if (not done[i] and 
                p.arrival_time <= current_time and 
                p.priority < best_priority):

                best_priority = p.priority
                idx = i

        # chưa có tiến trình nào tới
        if idx == -1:
            current_time += 1
            continue

        p = processes[idx]

        # nếu CPU rảnh trước khi process tới
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # tính toán theo đúng class Process
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.completion_time

        done[idx] = True
        completed += 1
        result_order.append(p.pid)

    return result_order, processes