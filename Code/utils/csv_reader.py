import csv
from models.process import Process

def read_csv(file_name):
    processes = []

    try:
        with open(file_name, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                p = Process(
                    pid=row['pid'],
                    arrival_time=int(row['arrival_time']),
                    burst_time=int(row['burst_time']),
                    priority=int(row['priority'])
                )
                processes.append(p)

    except FileNotFoundError:
        print("Không tìm thấy file")

    return processes