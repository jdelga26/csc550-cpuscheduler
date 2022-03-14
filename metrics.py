class Metrics:
    def __init__(self, workload, verbose):
        self.t = 0
        self.workload = {process['Process id']:process for process in workload}
        self.finishing_times = {}
        self.answer_times = {}
        self.starvation = {process['Process id']:[0] for process in workload}
        self.scheduler_runtime = 0
        self.context_switches = 0
        self.verbose = verbose

    def __str__(self):
        turnaround_times = {pid:(self.finishing_times[pid] - self.workload[pid]['Arrival Time'] + 1) for pid in self.workload.keys()}
        waiting_times = {pid:(turnaround_times[pid] - self.workload[pid]['Burst Time']) for pid in self.workload.keys()}
        throughput = len(self.workload) / self.t
        tail_starvation = max([max(self.starvation[pid]) for pid in self.starvation])

        if(self.verbose):
            priorities = sorted([process['Priority'] for process in self.workload.values()])
            upper_priorities = priorities[2*len(priorities)//3:-1]

            high_priority_starvation = {process['Process id']:self.starvation[process['Process id']] for process in self.workload.values() if process['Priority'] in upper_priorities}
            priority_tail_starvation = max([max(high_priority_starvation[pid]) for pid in high_priority_starvation])

            priority_waiting_times = [(turnaround_times[pid] - self.workload[pid]['Burst Time']) for pid in self.workload.keys() if self.workload[pid]['Priority'] in upper_priorities]
            avg_priority_waiting_time = round(sum(priority_waiting_times)/len(priority_waiting_times),2)

            return f"Total time: {self.t}\n" + \
               f"Throughput: {round(throughput, 5)}\n" + \
               f"Finishing times:\n\t{self.finishing_times}\n" + \
               f"Answer times:\n\t{self.answer_times}\n" + \
               f"Avg. Answer times: {sum(self.answer_times.values()) / len(self.workload)}\n" + \
               f"Turnaround times:\n\t{turnaround_times}\n" + \
               f"Avg. Turnaround times: {sum(turnaround_times.values()) / len(self.workload)}\n" + \
               f"Waiting times:\n\t{waiting_times}\n" + \
               f"Avg. Waiting times: {sum(waiting_times.values()) / len(self.workload)} \t\t({avg_priority_waiting_time} for top 1/3 priority)\n" + \
               f"Tail Latency: {tail_starvation} \t\t\t({priority_tail_starvation} for top 1/3 priority)\n" + \
               f"Scheduler runtime: {round(self.scheduler_runtime, 7)}\n" + \
               f"Context switches frequency: {round(self.context_switches/self.t,7)}"
        else:
            return f"Avg. Answer times: {sum(self.answer_times.values()) / len(self.workload)}\n" + \
                f"Avg. Turnaround times: {sum(turnaround_times.values()) / len(self.workload)}\n" + \
                f"Avg. Waiting times: {sum(waiting_times.values()) / len(self.workload)}\n" + \
                f"Tail Latency: {tail_starvation}\n" + \
                f"Scheduler runtime: {round(self.scheduler_runtime, 7)}\n" + \
                f"Context switches frequency: {round(self.context_switches/self.t,7)}"