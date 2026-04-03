import tkinter as tk
from tkinter import ttk, messagebox
import os
import copy
from datetime import datetime

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
            processes_copy = copy.deepcopy(self.processes)
            if self.algo_var.get() == "SJF":
                order, result = sjf_non_preemptive(processes_copy)
            else:
                order, result = priority_non_preemptive(processes_copy)

            self.current_result = result
            self.open_result_window(result, order)
            self.display_processes(result)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= EXPORT =================
    def export_csv(self):
        if not self.current_result:
            messagebox.showwarning("Warning", "Chưa có kết quả để xuất!")
            return

        os.makedirs(self.output_folder, exist_ok=True)
        filename = f"result_{self.algo_var.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        file_path = os.path.join(self.output_folder, filename)

        try:
            write_csv(self.current_result, file_path)
            messagebox.showinfo("Success", f"Đã lưu vào {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= RESULT WINDOW =================
    def open_result_window(self, processes, order):
        win = tk.Toplevel(self.root)
        win.title("Scheduling Result")
        win.geometry("1000x600")

        # ===== HEADER =====
        header_text = (
            f"File: {self.file_var.get()} | "
            f"Algorithm: {self.algo_var.get()} | "
            f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        tk.Label(
            win,
            text=header_text,
            font=("Arial", 11, "bold"),
            fg="black"
        ).pack(pady=5)

        # ===== AVERAGE =====
        avg_wt = sum(p.waiting_time for p in processes) / len(processes)
        avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
        avg_text = f"Average Waiting Time: {avg_wt:.2f} | Average Turnaround Time: {avg_tat:.2f}"

        tk.Label(
            win,
            text=avg_text,
            font=("Arial", 11)
        ).pack(pady=5)

        # ================= ORDER =================
        order_frame = tk.Frame(win)
        order_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        tk.Label(order_frame, text="Execution Order:", font=("Arial", 11, "bold")).pack(anchor="w")
        text_frame = tk.Frame(order_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        order_text = tk.Text(text_frame, height=10, wrap="word")
        scroll_y = tk.Scrollbar(text_frame, command=order_text.yview)
        order_text.configure(yscrollcommand=scroll_y.set)
        order_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        lines = []
        for i in range(0, len(order), 10):
            chunk = order[i:i+10]
            line = " → ".join(chunk)
            if i != 0:
                line = "→ " + line
            lines.append(line)

        order_text.insert(tk.END, "\n".join(lines))
        order_text.config(state="disabled")

        # ================= GANTT =================
        gantt_frame = tk.Frame(win)
        gantt_frame.pack(fill=tk.X, expand=False, padx=10, pady=5)
        tk.Label(gantt_frame, text="Gantt Chart:", font=("Arial", 11, "bold")).pack(anchor="w")
        canvas_frame = tk.Frame(gantt_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        canvas = tk.Canvas(canvas_frame, bg="white", height=220)
        scroll_x = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        canvas.configure(xscrollcommand=scroll_x.set)
        canvas.pack(fill=tk.BOTH, expand=True)
        scroll_x.pack(fill=tk.X)

        # ===== DRAG =====
        canvas.bind("<Button-1>", lambda e: canvas.scan_mark(e.x, e.y))
        canvas.bind("<B1-Motion>", lambda e: canvas.scan_dragto(e.x, e.y, gain=1))

        # ===== SCROLL NGANG BẰNG WHEEL =====
        def on_mousewheel(event):
            canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # ===== VẼ GANTT =====
        process_map = {p.pid: p for p in processes}

        scale = 20
        x = 10
        y_top = 60
        y_bottom = 120

        current_time = 0

        for pid in order:
            p = process_map[pid]

            if p.start_time > current_time:
                idle_duration = p.start_time - current_time
                idle_width = idle_duration * scale
                canvas.create_rectangle(
                    x, y_top, x + idle_width, y_bottom,
                    fill="#E0E0E0",
                    outline="black"
                )

                canvas.create_text(
                    x + idle_width / 2,
                    (y_top + y_bottom) / 2,
                    text="IDLE",
                    font=("Arial", 8)
                )

                canvas.create_text(
                    x,
                    y_bottom + 15,
                    text=str(current_time),
                    anchor="n"
                )

                x += idle_width
                current_time = p.start_time

            duration = p.completion_time - p.start_time
            width = max(duration * scale, 20)
            canvas.create_rectangle(
                x, y_top, x + width, y_bottom,
                fill="#90CAF9",
                outline="black"
            )

            if width < 30:
                canvas.create_text(
                    x + width / 2,
                    (y_top + y_bottom) / 2,
                    text=pid,
                    angle=90,
                    font=("Arial", 7)
                )
            else:
                canvas.create_text(
                    x + width / 2,
                    (y_top + y_bottom) / 2,
                    text=pid
                )
                canvas.create_text(
                    x,
                    y_bottom + 15,
                    text=str(p.start_time),
                    anchor="n"
                )

            x += width
            current_time = p.completion_time

        last = process_map[order[-1]]
        canvas.create_text(
            x,
            y_bottom + 15,
            text=str(last.completion_time),
            anchor="n"
        )

        canvas.configure(scrollregion=(0, 0, x + 50, 220))