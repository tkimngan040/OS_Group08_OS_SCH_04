import pandas as pd
import os

class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.data = None
        self.status = "IDLE"

    
    def load_data(self, file_path):
        """Nạp dữ liệu từ file thực tế"""
        if os.path.exists(file_path):
            try:
                self.data = pd.read_csv(file_path)
                self.status = "READY"
                print(f"[{self.process_name}] OK: Đã nạp dữ liệu từ {file_path}")
            except Exception as e:
                self.status = "ERROR"
                print(f"[{self.process_name}] LỖI: {e}")
        else:
            self.status = "NOT_FOUND"
            print(f"[{self.process_name}] CẢNH BÁO: File {file_path} không tồn tại!")

    def execute_task(self):


        
        if self.data is not None:
            self.status = "RUNNING"
            # Logic: Tính số dòng và cột
            rows, cols = self.data.shape
            print(f"[{self.process_name}] Đang xử lý: Tìm thấy {rows} dòng và {cols} cột.")
            self.status = "COMPLETED"
        else:
            print(f"[{self.process_name}] Thất bại: Không có dữ liệu để dọc.")

    def display_data(self):
        if self.data is not None:
            print(f"--- Nội dung {self.process_name} ---")
            print(self.data.head()) # In 5 dòng đầu
        else:
            print(f"[{self.process_name}] Không có dữ liệu để hiển thị.")
