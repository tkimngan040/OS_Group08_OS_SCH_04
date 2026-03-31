import tkinter as tk
from tkinter import ttk, messagebox
import os
import copy
import time

from utils.csv_reader import read_csv
from utils.csv_writer import write_csv
from algorithms.sjf import sjf_non_preemptive
from algorithms.priority import priority_non_preemptive


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling App")
        self.root.geometry("1000x700")

        self.processes = []
        self.current_result = []

        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.input_folder = os.path.join(base_dir, "input")
        self.output_folder = os.path.join(base_dir, "output")

        self.create_widgets()
        self.load_file_list()

    # ================= UI =================
    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # ===== FILE =====
        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(
            top_frame, textvariable=self.file_var,
            state="readonly", width=25
        )
        self.file_combo.grid(row=0, column=0, padx=5)

        tk.Button(top_frame, text="Load", command=self.load_file).grid(row=0, column=1, padx=5)

        # ===== ALGORITHM =====
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
        columns = (
            "Process ID",
            "Arrival Time",
            "Burst Time",
            "Priority",
            "Start Time",
            "Completion Time",
            "Waiting Time",
            "Turnaround Time"
        )
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== AVERAGE =====
        self.avg_label = tk.Label(
            self.root,
            text="Average Waiting Time: 0 | Average Turnaround Time:: 0",
            font=("Arial", 11)
        )
        self.avg_label.pack(pady=5)

        # ===== ORDER =====
        self.order_label = tk.Label(
            self.root,
            text="Execution Order: ",
            font=("Arial", 11)
        )
        self.order_label.pack(pady=5)

        # ===== GANTT =====
        self.gantt_label = tk.Label(
            self.root,
            text="Gantt Chart (CPU Scheduling Timeline)",
            bg="white",
            font=("Courier", 12),
            justify="left"
        )
        self.gantt_label.pack(fill=tk.X, padx=10, pady=10)

    # ================= LOAD FILE LIST =================
    def load_file_list(self):
        if not os.path.exists(self.input_folder):
            os.makedirs(self.input_folder)

        files = [f for f in os.listdir(self.input_folder) if f.endswith(".csv")]

        if files:
            self.file_combo["values"] = files
            self.file_combo.current(0)
        else:
            self.file_combo["values"] = []

    # ================= LOAD FILE =================
    def load_file(self):
        if not self.file_var.get():
            messagebox.showwarning("Warning", "Không có file CSV!")
            return

        file_path = os.path.join(self.input_folder, self.file_var.get())

        try:
            self.processes = read_csv(file_path)

            # reset UI
            self.current_result = []
            self.gantt_label.config(text="Gantt Chart (CPU Scheduling Timeline)")
            self.avg_label.config(text="Average Waiting Time: 0 | Average Turnaround Time: 0")
            self.order_label.config(text="Execution Order: ")

            self.display_processes(self.processes)

            messagebox.showinfo("Success", f"Đã load {self.file_var.get()}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= DISPLAY =================
    def display_processes(self, processes):
        for row in self.tree.get_children():
            self.tree.delete(row)

        # sort theo start_time để hiển thị đúng thứ tự chạy
        processes = sorted(processes, key=lambda p: p.start_time)

        for p in processes:
            self.tree.insert("", tk.END, values=(
                p.pid,
                p.arrival_time,
                p.burst_time,
                p.priority,
                p.start_time,
                p.completion_time,
                p.waiting_time,
                p.turnaround_time
            ))

    # ================= RUN =================
    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Chưa load dữ liệu!")
            return

        try:
            # deepcopy tránh bug
            processes_copy = copy.deepcopy(self.processes)

            if self.algo_var.get() == "SJF":
                order, result = sjf_non_preemptive(processes_copy)
            else:
                order, result = priority_non_preemptive(processes_copy)

            self.current_result = result

            self.display_processes(result)
            self.show_gantt(result, order)
            self.show_average(result)
            self.show_order(order)

            messagebox.showinfo("Done", "Chạy xong!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= GANTT =================
    def show_gantt(self, processes, order):
        chart = ""
        timeline = ""

        process_map = {p.pid: p for p in processes}

        for pid in order:
            p = process_map[pid]
            chart += f"| {p.pid} "
            timeline += f"{p.start_time}    "

        chart += "|"
        last = process_map[order[-1]]
        timeline += str(last.completion_time)

        self.gantt_label.config(text=chart + "\n" + timeline)

    # ================= AVERAGE =================
    def show_average(self, processes):
        avg_wt = sum(p.waiting_time for p in processes) / len(processes)
        avg_tat = sum(p.turnaround_time for p in processes) / len(processes)

        self.avg_label.config(
            text=f"Average Waiting Time: {avg_wt:.2f} | Average Turnaround Time: {avg_tat:.2f}"
        )

    # ================= ORDER =================
    def show_order(self, order):
        self.order_label.config(text="Execution Order: " + " → ".join(order))

    # ================= EXPORT =================
    def export_csv(self):
        if not self.current_result:
            messagebox.showwarning("Warning", "Chưa có kết quả để xuất!")
            return

        os.makedirs(self.output_folder, exist_ok=True)

        filename = f"result_{self.algo_var.get()}_{int(time.time())}.csv"
        file_path = os.path.join(self.output_folder, filename)

        try:
            write_csv(self.current_result, file_path)
            messagebox.showinfo("Success", f"Đã lưu vào {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))