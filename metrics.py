class Metrics:
    def __init__(self, processes):
        self.time_elapsed = 0
        self.processes_completed = 0
        self.turnaround_times = []
        self.waiting_times = []
    def get_results(self):
        throughput = self.processes_completed / self.time_elapsed
        avg_latency
        tail_latency
        scheduler_overhead
        return throughput