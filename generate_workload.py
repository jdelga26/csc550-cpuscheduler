import csv
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--outfile", help="The name of the file to output the workload to.", required=True, type=str)
parser.add_argument("-n", "--number_processes", help="The number of processes to simlate i a workload.", required=True, type=int)
parser.add_argument("-t", "--latest_arrival_time", help="The latest time in the workload at which new processes can arrive.", required=True, type=int)
parser.add_argument("-b", "--burst_time_range", help="The low and high for the generate.", nargs = 2, metavar=('burst_low', 'burst_high'), required=True, type=int)
parser.add_argument("-p", "--priority_range", help="The minimum and maximum priority for processes.", nargs = 2, metavar=('priority_low', 'priority_high'), required=True, type=int)

def main():
    args = parser.parse_args()
    filename = args.outfile
    num_processes = args.number_processes  
    latest_arrival_time = args.latest_arrival_time
    burst_low, burst_high = args.burst_time_range
    priority_low, priority_high = args.priority_range

    fields = ["Process id", "Burst Time", "Arrival Time", "Priority"]
    with open('workloads/'+filename+'.csv', 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields) 
        
        for i in range(num_processes):
            row = [i+1, random.randint(burst_low, burst_high), random.randint(0, latest_arrival_time), random.randint(priority_low, priority_high)]
            csvwriter.writerow(row)
    

if __name__ == '__main__':
    main()