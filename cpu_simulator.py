import os
import csv
import argparse

import fcfs
import sjf
import rr

algorithms = set(["FCFS", "SJF", "RR"])

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="The name of the CSV file containing a sample workload.", required=True, type=str)
parser.add_argument("-s", "--scheduler", help="The name of the scheduling algorithm to use.", required=True, type=str, choices=algorithms)

def main():
    args = parser.parse_args()
    workload_file = args.file  
    scheduler = args.scheduler
    
    workload_file = os.path.join('workflows',workload_file)
    if not os.path.isfile(workload_file):
        parser.error("The workload filename you specified was invalid.")

    if scheduler not in algorithms:
        parser.error("Invalid scheduler name.")

    with open(workload_file, 'r') as file:
        data = list(csv.reader(file))
        headers = data[0]
        workload = [dict(zip(headers,[int(num) for num in process])) for process in data[1:]]
        workload = sorted(workload, key=lambda x:x['Arrival Time'])
        globals()[scheduler.lower()].simulate(workload)

if __name__ == '__main__':
    main()