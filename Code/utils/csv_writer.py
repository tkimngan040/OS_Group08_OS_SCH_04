import pandas as pd

def write_csv(processes, file_path):
    data = []

    for p in processes:
        data.append({
            "pid": p.pid,
            "arrival_time": p.arrival_time,
            "burst_time": p.burst_time,
            "priority": p.priority,
            "start_time": p.start_time,
            "completion_time": p.completion_time,
            "waiting_time": p.waiting_time,
            "turnaround_time": p.turnaround_time
        })

    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)