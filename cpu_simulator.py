import os
import csv
import time
import argparse
from copy import deepcopy

from metrics import Metrics
import fcfs
import sjf
import rr
import bbq
import prr
import cfs_lite
import residual

algorithms = set(["fcfs", "sjf", "rr", "bbq", "prr", "cfs_lite", "residual"])

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The name of the CSV file containing a sample workload.", required=True, type=str)
parser.add_argument("-s", "--scheduler", help="The name of the scheduling algorithm to use.", required=True, type=str.lower, choices=algorithms)
parser.add_argument("-v", "--verbose", help="Output more information", default=False, action="store_true")

def simulate(workload, schedule, verbose):
    metrics = Metrics(deepcopy(workload), verbose)
    current_workload = deepcopy(workload)
    metrics.t = 0
    while len(current_workload) > 0:
        ready_queue = current_workload
        for i, process in enumerate(current_workload):
            if process["Arrival Time"] > metrics.t:
                ready_queue = current_workload[:i]
                break

        ready_ids = [process['Process id'] for process in ready_queue]

        if ready_queue != []:
            before_timestamp = time.time()
            i = ready_ids.index(schedule(ready_queue))

            metrics.scheduler_runtime += time.time() - before_timestamp
            if current_workload[i]['Process id'] not in metrics.answer_times.keys():
                metrics.answer_times[current_workload[i]['Process id']] = metrics.t

            if verbose:
                print(current_workload[i])
            current_workload[i]["Burst Time"] -= 1
            if(current_workload[i]["Burst Time"] == 0):
                metrics.finishing_times[current_workload[i]['Process id']] = metrics.t
                del current_workload[i]
        metrics.t += 1

    print(metrics)

def main():
    args = parser.parse_args()
    workload_file = args.file  
    scheduler = args.scheduler
    verbose = args.verbose
    
    workload_file = os.path.join('workloads',workload_file)
    if not os.path.isfile(workload_file):
        parser.error("The workload filename you specified was invalid.")

    if scheduler not in algorithms:
        parser.error("Invalid scheduler name.")

    with open(workload_file, 'r') as file:
        data = list(csv.reader(file))
        headers = data[0]
        workload = [dict(zip(headers,[int(num) for num in process])) for process in data[1:]]
        workload = sorted(workload, key=lambda x:x['Arrival Time'])

    simulate(workload, globals()[scheduler.lower()].schedule, verbose)

if __name__ == '__main__':
    main()