import pandas as pd
import os

class Process:
    def __init__(self, file_name):

        self.file_name = file_name
        self.data = None

    def load_data(self):
        """Hàm dùng để đọc dữ liệu từ file CSV"""


        # Kiểm tra xem file có tồn tại trong thư mục không
        if os.path.exists(self.file_name):
            try:
                # Đọc file bằng pandas
                self.data = pd.read_csv(self.file_name)
                print(f"--- [OK] Đã nạp dữ liệu từ file: {self.file_name} ---")
            except Exception as e:
                print(f"--- [LỖI] Không thể đọc nội dung file {self.file_name}: {e} ---")
        else:
            print(f"--- [CẢNH BÁO] File {self.file_name} không tồn tại trong thư mục này! ---")

    def display_data(self):
        #in dữ liệu ra màn hình
        if self.data is not None:
            print("Nội dung dữ liệu:")
            print(self.data)
            print("-" * 30)
        else:
            print(f"Chưa có dữ liệu để hiển thị cho DATA {self.file_name}.")

    def get_summary(self):

        if self.data is not None:
            rows, cols = self.data.shape
            print(f"File này có {rows} dòng và {cols} cột.")