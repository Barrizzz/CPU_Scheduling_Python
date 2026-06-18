import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from scheduler import Process, Scheduler

class CPU_Scheduling_App:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x800")
        
        self.scheduler = Scheduler()
        self.processes = []
        self.calculated_processes = []
        self.gantt_chart_data = []
        
        self._create_widgets()
        
    def _create_widgets(self):
        # Top Frame for Input
        input_frame = ttk.LabelFrame(self.root, text="Process Input")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Process ID:").grid(row=0, column=0, padx=5, pady=5)
        self.pid_entry = ttk.Entry(input_frame, width=10)
        self.pid_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5, pady=5)
        self.arrival_entry = ttk.Entry(input_frame, width=10)
        self.arrival_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Burst Time:").grid(row=0, column=4, padx=5, pady=5)
        self.burst_entry = ttk.Entry(input_frame, width=10)
        self.burst_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Priority:").grid(row=0, column=6, padx=5, pady=5)
        self.priority_entry = ttk.Entry(input_frame, width=10)
        self.priority_entry.grid(row=0, column=7, padx=5, pady=5)
        self.priority_entry.insert(0, "0") # Default priority
        
        add_btn = ttk.Button(input_frame, text="Add Process", command=self.add_process)
        add_btn.grid(row=0, column=8, padx=10, pady=5)
        
        clear_btn = ttk.Button(input_frame, text="Clear All", command=self.clear_processes)
        clear_btn.grid(row=0, column=9, padx=10, pady=5)
        
        # Middle Frame for Options and Table
        middle_frame = ttk.Frame(self.root)
        middle_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left side of Middle Frame: Options
        options_frame = ttk.LabelFrame(middle_frame, text="Scheduling Algorithm")
        options_frame.pack(side="left", fill="y", padx=5)
        
        self.algo_var = tk.StringVar(value="FCFS")
        algos = [("First Come First Serve", "FCFS"), 
                 ("Shortest Job First (Non-preemptive)", "SJF"),
                 ("Priority Scheduling (Non-preemptive)", "Priority"),
                 ("Round Robin", "RR")]
                 
        for text, val in algos:
            ttk.Radiobutton(options_frame, text=text, value=val, variable=self.algo_var).pack(anchor="w", padx=10, pady=5)
            
        tq_frame = ttk.Frame(options_frame)
        tq_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(tq_frame, text="Time Quantum (RR):").pack(side="left")
        self.tq_entry = ttk.Entry(tq_frame, width=5)
        self.tq_entry.pack(side="left", padx=5)
        self.tq_entry.insert(0, "2")
        
        simulate_btn = ttk.Button(options_frame, text="Simulate", command=self.simulate)
        simulate_btn.pack(pady=20, padx=10, fill="x")
        
        compare_btn = ttk.Button(options_frame, text="Compare All Algorithms", command=self.compare_all)
        compare_btn.pack(pady=5, padx=10, fill="x")
        
        # Right side of Middle Frame: Table
        table_frame = ttk.Frame(middle_frame)
        table_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        columns = ("pid", "arrival", "burst", "priority", "start", "completion", "turnaround", "waiting")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("pid", text="PID")
        self.tree.heading("arrival", text="Arrival")
        self.tree.heading("burst", text="Burst")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("start", text="Start")
        self.tree.heading("completion", text="Completion")
        self.tree.heading("turnaround", text="Turnaround")
        self.tree.heading("waiting", text="Waiting")
        
        self.tree.column("pid", width=50, anchor="center")
        self.tree.column("arrival", width=70, anchor="center")
        self.tree.column("burst", width=70, anchor="center")
        self.tree.column("priority", width=70, anchor="center")
        self.tree.column("start", width=70, anchor="center")
        self.tree.column("completion", width=80, anchor="center")
        self.tree.column("turnaround", width=80, anchor="center")
        self.tree.column("waiting", width=70, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Averages label
        self.avg_label = ttk.Label(table_frame, text="Avg Turnaround Time: 0.0 | Avg Waiting Time: 0.0", font=("Arial", 11, "bold"))
        self.avg_label.pack(pady=5)
        
        # Bottom Frame for Gantt Chart
        self.bottom_frame = ttk.LabelFrame(self.root, text="Gantt Chart & Visualization")
        self.bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
    def add_process(self):
        pid = self.pid_entry.get().strip()
        arrival = self.arrival_entry.get().strip()
        burst = self.burst_entry.get().strip()
        priority = self.priority_entry.get().strip()
        
        if not (pid and arrival and burst):
            messagebox.showerror("Input Error", "PID, Arrival Time, and Burst Time are required!")
            return
            
        try:
            arrival = int(arrival)
            burst = int(burst)
            priority = int(priority) if priority else 0
        except ValueError:
            messagebox.showerror("Input Error", "Times and Priority must be integers!")
            return
            
        # Check for duplicate PID
        for p in self.processes:
            if p.pid == pid:
                messagebox.showerror("Input Error", "Process ID already exists!")
                return
                
        p = Process(pid, arrival, burst, priority)
        self.processes.append(p)
        self.update_table(self.processes)
        
        # Clear entries
        self.pid_entry.delete(0, tk.END)
        self.arrival_entry.delete(0, tk.END)
        self.burst_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(0, "0")
        
    def clear_processes(self):
        self.processes = []
        self.calculated_processes = []
        self.update_table(self.processes)
        self.avg_label.config(text="Avg Turnaround Time: 0.0 | Avg Waiting Time: 0.0")
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
            
    def update_table(self, processes):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for p in processes:
            start = p.start_time if p.start_time != -1 else "-"
            comp = p.completion_time if p.completion_time != -1 else "-"
            self.tree.insert("", "end", values=(p.pid, p.arrival_time, p.burst_time, p.priority, start, comp, p.turnaround_time, p.waiting_time))
            
    def simulate(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add processes first!")
            return
            
        algo = self.algo_var.get()
        
        import copy
        procs_copy = copy.deepcopy(self.processes)
        
        if algo == "FCFS":
            result_procs, gantt = self.scheduler.fcfs(procs_copy)
        elif algo == "SJF":
            result_procs, gantt = self.scheduler.sjf(procs_copy)
        elif algo == "Priority":
            result_procs, gantt = self.scheduler.priority_scheduling(procs_copy)
        elif algo == "RR":
            try:
                tq = int(self.tq_entry.get())
                if tq <= 0: raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Time Quantum must be a positive integer!")
                return
            result_procs, gantt = self.scheduler.round_robin(procs_copy, tq)
            
        self.calculated_processes = result_procs
        self.gantt_chart_data = gantt
        
        self.update_table(result_procs)
        
        avg_ta = sum(p.turnaround_time for p in result_procs) / len(result_procs)
        avg_wt = sum(p.waiting_time for p in result_procs) / len(result_procs)
        
        self.avg_label.config(text=f"Avg Turnaround Time: {avg_ta:.2f} | Avg Waiting Time: {avg_wt:.2f}")
        
        self.draw_gantt_chart()
        
    def draw_gantt_chart(self):
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
            
        if not self.gantt_chart_data:
            return
            
        fig, ax = plt.subplots(figsize=(10, 2))
        
        colors = plt.cm.tab20.colors
        pid_to_color = {}
        color_idx = 0
        
        # Find max time
        max_time = max(end for _, _, end in self.gantt_chart_data)
        
        for pid, start, end in self.gantt_chart_data:
            if pid not in pid_to_color:
                pid_to_color[pid] = colors[color_idx % len(colors)]
                color_idx += 1
                
            ax.broken_barh([(start, end - start)], (10, 9), facecolors=(pid_to_color[pid]))
            ax.text(start + (end - start)/2, 14.5, pid, ha='center', va='center', color='black')
            
        ax.set_ylim(5, 25)
        ax.set_xlim(0, max_time + 1)
        ax.set_xlabel('Time')
        ax.set_yticks([])
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        xticks = set()
        for _, start, end in self.gantt_chart_data:
            xticks.add(start)
            xticks.add(end)
        ax.set_xticks(sorted(list(xticks)))
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.bottom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def compare_all(self):
        if not self.processes:
            messagebox.showwarning("Warning", "Please add processes first!")
            return
            
        import copy
        
        results = {}
        
        try:
            tq = int(self.tq_entry.get())
        except ValueError:
            tq = 2 # Default fallback
            
        # FCFS
        procs_fcfs, _ = self.scheduler.fcfs(copy.deepcopy(self.processes))
        results['FCFS'] = {
            'Avg WT': sum(p.waiting_time for p in procs_fcfs) / len(procs_fcfs),
            'Avg TAT': sum(p.turnaround_time for p in procs_fcfs) / len(procs_fcfs)
        }
        
        # SJF
        procs_sjf, _ = self.scheduler.sjf(copy.deepcopy(self.processes))
        results['SJF'] = {
            'Avg WT': sum(p.waiting_time for p in procs_sjf) / len(procs_sjf),
            'Avg TAT': sum(p.turnaround_time for p in procs_sjf) / len(procs_sjf)
        }
        
        # Priority
        procs_prio, _ = self.scheduler.priority_scheduling(copy.deepcopy(self.processes))
        results['Priority'] = {
            'Avg WT': sum(p.waiting_time for p in procs_prio) / len(procs_prio),
            'Avg TAT': sum(p.turnaround_time for p in procs_prio) / len(procs_prio)
        }
        
        # RR
        procs_rr, _ = self.scheduler.round_robin(copy.deepcopy(self.processes), tq)
        results['RR'] = {
            'Avg WT': sum(p.waiting_time for p in procs_rr) / len(procs_rr),
            'Avg TAT': sum(p.turnaround_time for p in procs_rr) / len(procs_rr)
        }
        
        # Plot comparison
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()
            
        fig, ax = plt.subplots(figsize=(10, 4))
        
        algos = list(results.keys())
        avg_wt = [results[a]['Avg WT'] for a in algos]
        avg_tat = [results[a]['Avg TAT'] for a in algos]
        
        x = range(len(algos))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], avg_wt, width, label='Average Waiting Time', color='skyblue')
        ax.bar([i + width/2 for i in x], avg_tat, width, label='Average Turnaround Time', color='salmon')
        
        ax.set_ylabel('Time')
        ax.set_title('Performance Comparison of Scheduling Algorithms')
        ax.set_xticks(x)
        ax.set_xticklabels(algos)
        ax.legend()
        
        # Add labels on top of bars
        for i, v in enumerate(avg_wt):
            ax.text(i - width/2, v + 0.1, f'{v:.2f}', ha='center', va='bottom')
        for i, v in enumerate(avg_tat):
            ax.text(i + width/2, v + 0.1, f'{v:.2f}', ha='center', va='bottom')
            
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.bottom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPU_Scheduling_App(root)
    root.mainloop()
