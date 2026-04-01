# csv_exporter.py
import csv
import os

def export_to_csv(processes):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "result.csv")

    fieldnames = [
        "pid",
        "arrival_time",
        "burst_time",
        "priority",
        "start_time",
        "completion_time",
        "turnaround_time",
        "waiting_time",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for p in processes:
            writer.writerow({
                "pid":              p.pid,
                "arrival_time":     p.arrival_time,
                "burst_time":       p.burst_time,
                "priority":         p.priority,
                "start_time":       p.start_time,
                "completion_time":  p.completion_time,
                "turnaround_time":  p.turnaround_time,
                "waiting_time":     p.waiting_time,
            })
