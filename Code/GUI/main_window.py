import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils.csv_reader import read_csv
from utils.csv_writer import write_csv
from algorithms.sjf import sjf_non_preemptive
from algorithms.priority import priority_non_preemptive


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling App")
        self.root.geometry("900x600")

        self.processes = []

        self.create_widgets()

    def create_widgets(self):
        # ===== TOP FRAME =====
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        # Load button
        tk.Button(top_frame, text="Load CSV", command=self.load_file).grid(row=0, column=0, padx=5)

        # Algorithm dropdown
        self.algo_var = tk.StringVar()
        self.algo_combo = ttk.Combobox(
            top_frame,
            textvariable=self.algo_var,
            values=["SJF", "Priority"],
            state="readonly"
        )
        self.algo_combo.grid(row=0, column=1, padx=5)
        self.algo_combo.current(0)

        # Run button
        tk.Button(top_frame, text="Run", command=self.run_algorithm).grid(row=0, column=2, padx=5)

        # Export button
        tk.Button(top_frame, text="Export CSV", command=self.export_csv).grid(row=0, column=3, padx=5)

        # ===== TABLE =====
        columns = ("PID", "AT", "BT", "Priority", "WT", "TAT")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== GANTT LABEL =====
        self.gantt_label = tk.Label(self.root, text="Gantt Chart will appear here", bg="white")
        self.gantt_label.pack(fill=tk.X, padx=10, pady=10)

    # ===== FUNCTIONS =====

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            self.processes = read_csv(file_path)
            self.display_processes(self.processes)
            messagebox.showinfo("Success", "Load file thành công!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_processes(self, processes):
        # clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # insert data
        for p in processes:
            self.tree.insert("", tk.END, values=(
                p.pid,
                p.arrival_time,
                p.burst_time,
                p.priority,
                p.waiting_time,
                p.turnaround_time
            ))

    def run_algorithm(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Chưa load file!")
            return

        algo = self.algo_var.get()

        try:
            if algo == "SJF":
                order, result = sjf_non_preemptive(self.processes)
            else:
                order, result = priority_non_preemptive(self.processes)

            self.display_processes(result)
            self.show_gantt(order)

            messagebox.showinfo("Done", "Chạy xong!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_gantt(self, order):
        text = " | ".join(order)
        self.gantt_label.config(text=f"Gantt: {text}")

    def export_csv(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Không có dữ liệu!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv")

        if not file_path:
            return

        try:
            write_csv(self.processes, file_path)
            messagebox.showinfo("Success", "Xuất file thành công!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ===== RUN APP =====
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()