from process import Process


def run_program():
    print("=== HỆ THỐNG ĐATJ TÊN LẠI SAU ===")

    # Danh sách các file cần xử lý
    files = ["data1.csv", "data.csv", "data3.csv"]

    

    # Tạo các đối tượng Process khác nhau
    for i, file_name in enumerate(files, 1):
        print(f"\n--- Bắt đầu đọc dữ liệu {i} ---")


        p = Process(f"Đọc data_{i}")


        p.load_data(file_name)  # ĐỌC (data1.csv) ỞE DÂY
        p.execute_task()
        p.display_data()

    print("\n hoàn thành")


if __name__ == "__main__":
    run_program()
