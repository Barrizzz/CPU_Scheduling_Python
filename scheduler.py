class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Computed properties
        self.start_time = -1
        self.completion_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        
        # For tracking remaining time in preemptive/RR
        self.remaining_time = burst_time

    def reset(self):
        self.start_time = -1
        self.completion_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = self.burst_time

class Scheduler:
    def __init__(self):
        self.gantt_chart = [] # List of tuples: (pid, start_time, end_time)
        
    def _reset_processes(self, processes):
        for p in processes:
            p.reset()
        self.gantt_chart = []
        
    def fcfs(self, processes):
        self._reset_processes(processes)
        # Sort by arrival time
        processes = sorted(processes, key=lambda x: x.arrival_time)
        
        current_time = 0
        for p in processes:
            if current_time < p.arrival_time:
                current_time = p.arrival_time
                
            p.start_time = current_time
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            
            self.gantt_chart.append((p.pid, current_time, p.completion_time))
            current_time = p.completion_time
            
        return processes, self.gantt_chart
        
    def sjf(self, processes): # Non-preemptive
        self._reset_processes(processes)
        
        n = len(processes)
        completed = 0
        current_time = 0
        is_completed = [False] * n
        
        while completed < n:
            # Find process with minimum burst time among arrived processes
            idx = -1
            min_burst = float('inf')
            
            for i in range(n):
                if not is_completed[i] and processes[i].arrival_time <= current_time:
                    if processes[i].burst_time < min_burst:
                        min_burst = processes[i].burst_time
                        idx = i
                        
            if idx != -1:
                p = processes[idx]
                p.start_time = current_time
                p.completion_time = current_time + p.burst_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                
                self.gantt_chart.append((p.pid, current_time, p.completion_time))
                current_time = p.completion_time
                is_completed[idx] = True
                completed += 1
            else:
                current_time += 1 # Idle CPU
                
        return processes, self.gantt_chart
        
    def priority_scheduling(self, processes): # Non-preemptive, Lower number = Higher Priority
        self._reset_processes(processes)
        
        n = len(processes)
        completed = 0
        current_time = 0
        is_completed = [False] * n
        
        while completed < n:
            idx = -1
            min_priority = float('inf')
            
            for i in range(n):
                if not is_completed[i] and processes[i].arrival_time <= current_time:
                    if processes[i].priority < min_priority:
                        min_priority = processes[i].priority
                        idx = i
                        
            if idx != -1:
                p = processes[idx]
                p.start_time = current_time
                p.completion_time = current_time + p.burst_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                
                self.gantt_chart.append((p.pid, current_time, p.completion_time))
                current_time = p.completion_time
                is_completed[idx] = True
                completed += 1
            else:
                current_time += 1 # Idle CPU
                
        return processes, self.gantt_chart
        
    def round_robin(self, processes, time_quantum):
        self._reset_processes(processes)
        
        n = len(processes)
        current_time = 0
        completed = 0
        
        # Sort by arrival time initially
        processes = sorted(processes, key=lambda x: x.arrival_time)
        ready_queue = []
        is_in_queue = [False] * n
        
        # Check initially arrived processes
        i = 0
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(i)
            is_in_queue[i] = True
            i += 1
            
        while completed < n:
            if not ready_queue:
                current_time += 1
                while i < n and processes[i].arrival_time <= current_time:
                    ready_queue.append(i)
                    is_in_queue[i] = True
                    i += 1
                continue
                
            idx = ready_queue.pop(0)
            p = processes[idx]
            
            if p.start_time == -1:
                p.start_time = current_time
                
            time_to_run = min(time_quantum, p.remaining_time)
            self.gantt_chart.append((p.pid, current_time, current_time + time_to_run))
            current_time += time_to_run
            p.remaining_time -= time_to_run
            
            # Check newly arrived processes while this process was executing
            while i < n and processes[i].arrival_time <= current_time:
                ready_queue.append(i)
                is_in_queue[i] = True
                i += 1
                
            if p.remaining_time > 0:
                ready_queue.append(idx)
            else:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed += 1
                
        # Consolidate Gantt chart fragments of same process
        consolidated_gantt = []
        for segment in self.gantt_chart:
            if consolidated_gantt and consolidated_gantt[-1][0] == segment[0] and consolidated_gantt[-1][2] == segment[1]:
                consolidated_gantt[-1] = (segment[0], consolidated_gantt[-1][1], segment[2])
            else:
                consolidated_gantt.append(segment)
                
        self.gantt_chart = consolidated_gantt
        
        return processes, self.gantt_chart
