class Scheduler:
    def __init__(self):
        self.gantt_chart = [] # List of tuples: (pid, start_time, end_time)

    def _reset_processes(self, processes):
        # This function is to reset each processes in the list of processes
        for p in processes:
            p.reset()
        self.gantt_chart = []
        
    def fcfs(self, processes):
        # FCFS = First Come First Serve
        self._reset_processes(processes)
        # Sort the processes by arrival time using lambda function
        processes = sorted(processes, key=lambda x: x.arrival_time)
        
        # Track the time
        current_time = 0
        for p in processes:
            # If the process hasn't arrived yet, skip time forward to its arrival time
            if current_time < p.arrival_time:
                current_time = p.arrival_time
                
            # Set the start time, completion time, turnaround time, and waiting time
            p.start_time = current_time
            p.completion_time = current_time + p.burst_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            
            self.gantt_chart.append((p.pid, current_time, p.completion_time))
            current_time = p.completion_time  # move clock forward to when this one finished
            
        return processes, self.gantt_chart
        
    def sjf(self, processes, is_priority=False): 
        # SJF = Shortest Job First
        # sorting the processes according to the smallest burst time first
        self._reset_processes(processes)
        
        # Keep track of the number of processes, how many are done, and the current time
        n = len(processes)
        completed = 0
        current_time = 0
        is_completed = [False] * n  # keeps track of which processes are already done
        
        # loop until all processes are completed
        while completed < n:
            # look through all processes and find the shortest one that has arrived
            idx = -1
            min_val = float('inf')
            
            # finds the process with the shortest burst time that has arrived
            for i in range(n):
                # if process is not completed and has arrived
                if not is_completed[i] and processes[i].arrival_time <= current_time:
                    # FOR PRIORITY SCHEDULING
                    if is_priority:
                        # if the process has a smaller priority than the current minimum
                        if processes[i].priority < min_val:
                            # update the minimum priority and the index of the process
                            min_val = processes[i].priority
                            idx = i
                        # Tie-breaker: If priorities are equal, choose the one that arrived first (FCFS)
                        elif processes[i].priority == min_val and idx != -1:
                            if processes[i].arrival_time < processes[idx].arrival_time:
                                idx = i
                    # FOR SHORTEST JOB FIRST
                    else:
                        # if the process has a smaller burst time than the current minimum
                        if processes[i].burst_time < min_val:
                            # update the minimum burst time and the index of the process
                            min_val = processes[i].burst_time
                            idx = i
                        # Tie-breaker: If burst times are equal, choose the one that arrived first (FCFS)
                        elif processes[i].burst_time == min_val and idx != -1:
                            if processes[i].arrival_time < processes[idx].arrival_time:
                                idx = i
                        
            # if there is a process to run
            if idx != -1:
                # take the process
                p = processes[idx]
                # set the start time, completion time, turnaround time, and waiting time
                p.start_time = current_time
                p.completion_time = current_time + p.burst_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                
                # append to the gantt chart attribute
                self.gantt_chart.append((p.pid, current_time, p.completion_time))
                # update current time, completed status
                current_time = p.completion_time
                is_completed[idx] = True
                completed += 1
            else:
                # Nothing has arrived yet, jump directly to the next arrival time
                next_arrival = float('inf')
                for i in range(n):
                    if not is_completed[i] and processes[i].arrival_time > current_time:
                        if processes[i].arrival_time < next_arrival:
                            next_arrival = processes[i].arrival_time
                current_time = next_arrival
                
        return processes, self.gantt_chart
        
    def priority_scheduling(self, processes): 
        # It seems that priority scheduling algorithm is very similar to sjf
        # The only difference being that priority scheduling is based on the lowest number of priority first meanwhile sjf is on the burst time
        # So I decided to refactor the code for this to just use the same function to avoid repetition
        return self.sjf(processes, is_priority=True)
        
    def round_robin(self, processes, time_quantum):
        # Round Robin = everyone gets a turn for a fixed slice of time (time_quantum)
        # then gets sent to the back of the line if not done yet. fair scheduling basically
        self._reset_processes(processes)
        
        n = len(processes)
        current_time = 0
        completed = 0
        
        # Sort by arrival time initially
        processes = sorted(processes, key=lambda x: x.arrival_time)
        ready_queue = []  # holds index of processes that are waiting for cpu
        is_in_queue = [False] * n
        
        # Check initially arrived processes
        # before we even start, add anyone who already arrived at time 0 to the queue
        i = 0
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(i)
            is_in_queue[i] = True
            i += 1
            
        # main loop until all processes are completed
        while completed < n:
            # if queue is empty, move time forward to next arrival
            if not ready_queue:
                # queue is empty but processes still left, means cpu has nothing to do
                # so tick the clock and check if new processes arrived
                current_time += 1
                while i < n and processes[i].arrival_time <= current_time:
                    ready_queue.append(i)
                    is_in_queue[i] = True
                    i += 1
                continue
                
            # take the process at front of the queue (since RR uses FIFO queue logic)
            idx = ready_queue.pop(0)
            p = processes[idx]
            
            # only set start_time the FIRST time this process ever runs
            # because round robin can run the same process multiple times in chunks
            if p.start_time == -1:
                p.start_time = current_time
                
            # run it for either the full time_quantum, or whatever time it has left
            # (whichever is smaller, since it might finish before the quantum is up)
            time_to_run = min(time_quantum, p.remaining_time)
            self.gantt_chart.append((p.pid, current_time, current_time + time_to_run))
            current_time += time_to_run
            p.remaining_time -= time_to_run
            
            # Check newly arrived processes while this process was executing
            # new processes might have shown up while we were running this chunk
            while i < n and processes[i].arrival_time <= current_time:
                ready_queue.append(i)
                is_in_queue[i] = True
                i += 1
                
            if p.remaining_time > 0:
                # still has work left, so send it back to the end of the queue
                ready_queue.append(idx)
            else:
                # done! now we can finally calculate its stats for real
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed += 1
                
        # Consolidate Gantt chart fragments of same process
        # round robin chops up one process into many small chunks in the gantt chart
        # this part just glues back-to-back chunks of the SAME process into one block
        # so the chart looks cleaner instead of showing tiny broken pieces
        consolidated_gantt = []
        for segment in self.gantt_chart:
            if consolidated_gantt and consolidated_gantt[-1][0] == segment[0] and consolidated_gantt[-1][2] == segment[1]:
                consolidated_gantt[-1] = (segment[0], consolidated_gantt[-1][1], segment[2])
            else:
                consolidated_gantt.append(segment)
                
        self.gantt_chart = consolidated_gantt
        
        return processes, self.gantt_chart