from utils.csv_reader import read_csv

def main():
    files = ["../input/data1.csv", "../input/data2.csv", "../input/data3.csv"]

    for file in files:
        print(f"\n=== Đang đọc {file} ===")

        processes = read_csv(file)

        if not processes:
            print("Không có dữ liệu")
            continue

        for p in processes:
            print(p.pid, p.arrival_time, p.burst_time, p.priority)

if __name__ == "__main__":
    main()