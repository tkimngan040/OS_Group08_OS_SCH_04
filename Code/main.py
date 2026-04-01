from GUI.main_window import App
import tkinter as tk

root = tk.Tk()
app = App(root)
root.mainloop()
#phan nay de tao ra file result
from process import Process
from sjf import sjf_non_preemptive
from csv_exporter import export_to_csv

processes = [Process("P1", 0, 6), Process("P2", 1, 4), Process("P3", 2, 2)]
order, result = sjf_non_preemptive(processes)
export_to_csv(result)
