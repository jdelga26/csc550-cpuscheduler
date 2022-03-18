import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from collections import defaultdict
import warnings
import math

warnings.filterwarnings('ignore')

rr_queue = []
time_slice = 10
remaining_time = time_slice
threshold = 10
time_slices = {}
max_cluster = 10

def get_adjust_time_slices(ready_queue):
    # data preparation
    queue_1 = sorted(ready_queue, key=lambda x:x['Burst Time'])[:len(ready_queue) // 2]
    queue_2 = sorted(ready_queue, key=lambda x:x['Burst Time'])[len(ready_queue) // 2:]
    
    total_burst_times = sum([process['Burst Time'] for process in ready_queue])
    process_weights = {process['Process id']:(process['Burst Time'] / total_burst_times) for process in ready_queue}
    
    num_context_switches = {process['Process id']:((process['Burst Time'] // time_slice) if (process['Burst Time'] % time_slice != 0) else (process['Burst Time'] // time_slice) - 1) for process in ready_queue}
    
    permitted_time_quanta = {process['Process id']:min(process['Burst Time'], time_slice) for process in ready_queue}
    proportional_burst_time = {process['Process id']:(process['Burst Time'] / sum(permitted_time_quanta.values())) for process in ready_queue}

    proportional_time_slice = {process['Process id']:(1 - proportional_burst_time[process['Process id']]) * time_slice for process in ready_queue}

    # silhouette method
    dataset = []

    for process in ready_queue:
        pid = process['Process id']
        dataset.append([process['Burst Time'], process_weights[pid], permitted_time_quanta[pid], proportional_burst_time[pid], num_context_switches[pid], proportional_time_slice[pid]])

    silhouette_coefficient = 0
    max_n = 0
    for n in range(2, min(len(ready_queue), max_cluster)):
        kmeans = KMeans(n_clusters=n, random_state=0).fit(dataset)
        new = metrics.silhouette_score(dataset, kmeans.labels_)
        if new > silhouette_coefficient:
            silhouette_coefficient = new
            max_n = n

    # k-means clustering
    kmeans = KMeans(n_clusters=max_n, random_state=0).fit(dataset)

    clusters = defaultdict(list)
    for label, process in zip(kmeans.labels_, ready_queue):
        clusters[label].append(process)

    cluster_average_burst_time = {label:sum([process['Burst Time'] for process in clusters[label]]) for label in clusters}

    cluster_weights = {label:cluster_average_burst_time[label] / sum(cluster_average_burst_time.values()) for label in clusters}
    cluster_time_slice = {label:(1 - (cluster_weights[label] / sum(cluster_weights.values()))) * time_slice for label in clusters}
    process_time_slice = {process['Process id']:math.ceil(cluster_time_slice[label]) for label, process in zip(kmeans.labels_, ready_queue)}

    # dynamic implementations

    for process in ready_queue:
        pid = process['Process id']
        if threshold * ((process['Burst Time'] / time_slice) + 1) >= process['Burst Time'] % process_time_slice[pid] \
            and process['Burst Time'] % process_time_slice[pid] > 0 \
            and process['Burst Time'] in queue_1:

            process_time_slice[pid] += threshold
    
    return process_time_slice

def schedule(ready_queue):
    global rr_queue
    global remaining_time
    global time_slices

    # ATS requires 3 or more processes to cluster. The processes also need to not all have identical burst times for the silhouette scoring to work. The behavior for this case is not defined in the paper, and while it is quite rare it *does* happen once in one of the randomly generated workloads.
    if len(ready_queue) < 3 or all([process['Burst Time'] == ready_queue[0]['Burst Time'] for process in ready_queue]):
        return ready_queue[0]['Process id']

    if not rr_queue:
        rr_queue = ready_queue

    if not time_slices:
        time_slices = get_adjust_time_slices(ready_queue)
        remaining_time = time_slices[rr_queue[0]["Process id"]]

    if rr_queue:
        to_add = [process for process in ready_queue if process not in rr_queue]
        if to_add:
            rr_queue.extend(to_add)
        to_subtract = [process for process in rr_queue if process not in ready_queue]
        if to_subtract:
            rr_queue.remove(to_subtract[0])
        if (to_add or to_subtract) and len(ready_queue) >= 3:
            if all([process['Burst Time'] == ready_queue[0]['Burst Time'] for process in ready_queue]):
                time_slices = {}
                return ready_queue[0]['Process id']
            else:
                time_slices = get_adjust_time_slices(ready_queue)
        if to_subtract:
            remaining_time = time_slices[rr_queue[0]["Process id"]]

    if not remaining_time:
        remaining_time = time_slices[rr_queue[1]["Process id"]]
        rr_queue.append(rr_queue[0])
        del rr_queue[0]

    remaining_time -= 1
    return rr_queue[0]['Process id']