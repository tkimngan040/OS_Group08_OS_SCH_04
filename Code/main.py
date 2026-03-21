from process import Process


def run_program():
    print("=== CHƯƠNG TRÌNH CÓ TÊN ĐỂ Vô SAU ===")


    print("\n--- data1.csv ---")
    p1 = Process("data1.csv")
    p1.load_data()
    p1.display_data()  #  in dữ liệu ra xem


    print("\n--- data2.csv ---")
    p2 = Process("data.csv")
    p2.load_data()
    p2.display_data()


    print("\n--- data3.csv ---")
    p3 = Process("data3.csv")
    p3.load_data()
    p3.display_data()
    print("\n=== Hoàn thành nhiệm vụ! ===")


if __name__ == "__main__":
    run_program()