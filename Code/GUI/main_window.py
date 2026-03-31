import tkinter as tk
from tkinter import ttk, messagebox
import os

from utils.csv_reader import read_csv
from utils.csv_writer import write_csv
from algorithms.sjf import sjf_non_preemptive
from algorithms.priority import priority_non_preemptive


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling App")
        self.root.geometry("950x650")

        self.processes = []
        self.current_result = []

        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.input_folder = os.path.join(base_dir, "input")
        self.output_folder = os.path.join(base_dir, "output")

        self.create_widgets()
        self.load_file_list()

    # ===== UI =====
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # chọn file CSV trong input/
        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(top_frame, textvariable=self.file_var, state="readonly", width=25)
        self.file_combo.grid(row=0, column=0, padx=5)

        tk.Button(top_frame, text="Load", command=self.load_file).grid(row=0, column=1, padx=5)

        # chọn thuật toán
        self.algo_var = tk.StringVar()
        self.algo_combo = ttk.Combobox(
            top_frame,
            textvariable=self.algo_var,
            values=["SJF", "Priority"],
            state="readonly",
            width=15
        )
        self.algo_combo.grid(row=0, column=2, padx=5)
        self.algo_combo.current(0)

        tk.Button(top_frame, text="Run", command=self.run_algorithm).grid(row=0, column=3, padx=5)
        tk.Button(top_frame, text="Export", command=self.export_csv).grid(row=0, column=4, padx=5)

        # ===== TABLE =====
        columns = ("PID", "AT", "BT", "Priority", "WT", "TAT")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== AVG RESULT =====
        self.avg_label = tk.Label(self.root, text="Average WT: 0 | Average TAT: 0", font=("Arial", 11))
        self.avg_label.pack(pady=5)

        # ===== GANTT =====
        self.gantt_label = tk.Label(self.root, text="Gantt Chart", bg="white", font=("Courier", 12))
        self.gantt_label.pack(fill=tk.X, padx=10, pady=10)

    # ===== LOAD FILE LIST =====
    def load_file_list(self):
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)

        files = [f for f in os.listdir(self.input_folder) if f.endswith(".csv")]

        if files:
            self.file_combo["values"] = files
            self.file_combo.current(0)
        else:
            self.file_combo["values"] = []

    # ===== LOAD FILE =====
    def load_file(self):
        if not self.file_var.get():
            messagebox.showwarning("Warning", "Không có file CSV!")
            return

        file_path = os.path.join(self.input_folder, self.file_var.get())

        try:
            self.processes = read_csv(file_path)
            self.display_processes(self.processes)
            messagebox.showinfo("Success", f"Đã load {self.file_var.get()}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===== DISPLAY =====
    def display_processes(self, processes):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in processes:
            self.tree.insert("", tk.END, values=(
                p.pid,
                p.arrival_time,
                p.burst_time,
                p.priority,
                p.waiting_time,
                p.turnaround_time
            ))

    # ===== RUN =====
    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Chưa load dữ liệu!")
            return

        try:
            if self.algo_var.get() == "SJF":
                order, result = sjf_non_preemptive(self.processes)
            else:
                order, result = priority_non_preemptive(self.processes)

            self.current_result = result

            self.display_processes(result)
            self.show_gantt(result)
            self.show_average(result)

            messagebox.showinfo("Done", "Chạy xong!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ===== GANTT =====
    def show_gantt(self, processes):
        chart = ""
        timeline = "0"

        for p in processes:
            chart += f"| {p.pid} "
            timeline += f"    {p.completion_time}"

        chart += "|"

        self.gantt_label.config(text=chart + "\n" + timeline)

    # ===== AVERAGE =====
    def show_average(self, processes):
        avg_wt = sum(p.waiting_time for p in processes) / len(processes)
        avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

        self.avg_label.config(
            text=f"Average WT: {avg_wt:.2f} | Average TAT: {avg_tat:.2f}"
        )

    # ===== EXPORT =====
    def export_csv(self):
        if not self.current_result:
            messagebox.showwarning("Warning", "Chưa có kết quả để xuất!")
            return

        os.makedirs(self.output_folder, exist_ok=True)

        filename = f"result_{self.algo_var.get()}.csv"
        file_path = os.path.join(self.output_folder, filename)

        try:
            write_csv(self.current_result, file_path)
            messagebox.showinfo("Success", f"Đã lưu vào {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ===== RUN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()