# This object represent a single process
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        # The input values
        self.pid = pid                    
        self.arrival_time = arrival_time  
        self.burst_time = burst_time     
        self.priority = priority          
        
        # These computed values are not known yet when we create the process
        # These values will be filled in later once the scheduling algorithm runs
        self.start_time = -1        # -1 means "hasn't started yet"
        self.completion_time = -1   # -1 means "hasn't finished yet"
        self.waiting_time = 0
        self.turnaround_time = 0
        
        # This one is for RR
        # Round robin can pause a process mid way and come back to it later,
        # so we need to track how much burst time is left, not just the total
        self.remaining_time = burst_time

    # help function to reset the computed values
    def reset(self):
        self.start_time = -1
        self.completion_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0
        self.remaining_time = self.burst_time
