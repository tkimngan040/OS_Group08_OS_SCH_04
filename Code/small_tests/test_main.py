from utils.csv_reader import read_csv
from utils.csv_writer import write_csv
from utils.process import calculate_times
from utils.process import calculate_times

# đọc file
processes = read_csv("../input/data1.csv")

# test in ra
print("=== INPUT ===")
for p in processes:
    print(p)

# giả lập xử lý (FCFS)
processes = calculate_times(processes)

# in kết quả
print("\n=== OUTPUT ===")
for p in processes:
    print(f"{p.pid}: WT={p.waiting_time}, TAT={p.turnaround_time}")

# ghi ra file
write_csv(processes, "output.csv")