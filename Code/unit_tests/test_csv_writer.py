import unittest
import os
import sys
import pandas as pd

# Thêm thư mục gốc vào sys.path để Python tìm thấy các module models và utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.process import Process
from utils.csv_writer import write_csv

class TestCSVWriter(unittest.TestCase):
    def setUp(self):
        """Hàm này chạy TRƯỚC mỗi test case để chuẩn bị môi trường."""
        # Bỏ tạo thư mục output, chỉ ghi ra file tạm ở thư mục hiện tại
        self.test_file = "test_result.csv"

        # Tạo sẵn dữ liệu 2 tiến trình để test
        self.processes = [
            Process("P1", 0, 5, 1),
            Process("P2", 1, 3, 2)
        ]
        
        # Điền số liệu giả lập sau khi đã chạy thuật toán
        self.processes[0].start_time = 0
        self.processes[0].completion_time = 5
        self.processes[0].waiting_time = 0
        self.processes[0].turnaround_time = 5

        self.processes[1].start_time = 5
        self.processes[1].completion_time = 8
        self.processes[1].waiting_time = 4
        self.processes[1].turnaround_time = 7

    def test_write_csv_success(self):
        """Kiểm tra xem hàm write_csv có tạo file và ghi đúng dữ liệu không."""
        # Chạy hàm cần test
        write_csv(self.processes, self.test_file)

        # 1. Kiểm tra xem file có thực sự được tạo ra trên ổ cứng không
        self.assertTrue(os.path.exists(self.test_file), "Lỗi: File CSV chưa được tạo!")

        # 2. Đọc ngược file lại bằng pandas để kiểm tra nội dung bên trong
        df = pd.read_csv(self.test_file)

        # Kiểm tra tổng số dòng dữ liệu (phải là 2 dòng)
        self.assertEqual(len(df), 2, "Lỗi: Số lượng dòng ghi ra không khớp với dữ liệu truyền vào.")

        # Kiểm tra xem có đủ cột theo đúng thứ tự không
        expected_columns = ["pid", "arrival_time", "burst_time", "priority", 
                            "start_time", "completion_time", "waiting_time", "turnaround_time"]
        self.assertListEqual(list(df.columns), expected_columns, "Lỗi: Sai tên cột hoặc thiếu cột.")

        # Kiểm tra dữ liệu của P1 xem có đúng không
        self.assertEqual(df.iloc[0]["pid"], "P1")
        self.assertEqual(df.iloc[0]["completion_time"], 5)

    def tearDown(self):
        """Hàm này chạy SAU mỗi test case để dọn dẹp rác."""
        # Xóa file test đi để trả lại môi trường sạch sẽ
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()
