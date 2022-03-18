# "Differently Fair Scheduler"
# Random new algorithm idea, similar to CFS but also not. Just because.
# Basically computes a score for each process and always runs the highest scoring one. Score is based on things like how much CPU time the process has already been given, the current latency of that process, and whether or not running that process would require a context switch.
# For a real-life implementation you would want to do calculations to predict *when* the process will no longer have the highest score, and just keep running it until that point without recalculating with each step. That would incur rather less overhead. But for the purposes of just testing this thing, meh.

import math
import sys

runtimes = {}
waittimes = {}

base_context_switch_penalty = 50
context_switch_penalty = base_context_switch_penalty
priority_factor = 1.25

normalized_runtime_weight = 0.8
normalized_latency_weight = 0.2

pid_running = None

def schedule(ready_queue):
    global pid_running
    global runtimes
    global waittimes
    global context_switch_penalty
    
    context_switch_penalty = round(base_context_switch_penalty * math.log(len(ready_queue)))

    ready_pids = [process['Process id'] for process in ready_queue]
    priorities = {process['Process id']:process['Priority'] for process in ready_queue}

    for pid in ready_pids:
        if pid not in runtimes.keys():
            if len(runtimes):
                runtimes[pid] = min(runtimes.values())
            else:
                runtimes[pid] = 0
            waittimes[pid] = sys.maxsize
    
    vlatencies = [context_switch_penalty if pid == pid_running else waittimes[pid] for pid in ready_pids]
    vlatencies = [vlatency*(priority_factor**priorities[pid]) for vlatency,pid in zip(vlatencies,ready_pids)]
    normalized_vlatencies = [latency/(max(vlatencies)+1) for latency in vlatencies]
    normalized_vlatencies = [1-latency for latency in normalized_vlatencies]

    vruntimes = [runtimes[pid]+context_switch_penalty if pid == pid_running else runtimes[pid] for pid in ready_pids]
    vruntimes = [vruntime*(priority_factor**priorities[pid]) for vruntime,pid in zip(vruntimes,ready_pids)]
    normalized_vruntimes = [runtime/(max(vruntimes)+1) for runtime in vruntimes]

    weights = [normalized_runtime_weight*runtime + normalized_latency_weight*latency for runtime,latency in zip(normalized_vlatencies,normalized_vruntimes)]

    pid_running = ready_pids[weights.index(min(weights))]
    runtimes[pid_running] += 1
    waittimes[pid_running] = 0

    for pid in ready_pids:
        if pid != pid_running:
            waittimes[pid] += 1

    return pid_running