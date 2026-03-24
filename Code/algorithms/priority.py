def priority_non_preemptive(processes):
    n = len(processes)

    current_time = 0
    done = [False] * n
    result_order = []

    while len(result_order) < n:
        idx = -1
        best_priority = float('inf')
        # tìm tiến trình phù hợp
        for i in range(n):
            if not done[i] and processes[i]['arrival'] <= current_time:
                if processes[i]['priority'] < best_priority:
                    best_priority = processes[i]['priority']
                    idx = i

        if idx == -1:
            current_time += 1
            continue

        p = processes[idx]

        # tính toán
        p['waiting'] = current_time - p['arrival']
        current_time += p['burst']
        p['turnaround'] = p['waiting'] + p['burst']

        done[idx] = True
        result_order.append(p['id'])

    return result_order, processes