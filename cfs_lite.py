from collections import defaultdict

vruntimes = defaultdict(float)
pid_running = None
t = 0

def schedule(ready_queue):
    global pid_running
    global vruntimes
    global t

    t += 1
    ready_pids = [process['Process id'] for process in ready_queue]
    
    if pid_running in ready_pids:
        ideal_runtime = sum([vruntimes[pid] for pid in ready_pids]) / len(ready_queue)
        if vruntimes[pid_running] <= ideal_runtime:
            return pid_running

    [vruntimes[i] for i in ready_pids]
    pid_running = min(ready_pids, key=vruntimes.get)
    process = ready_queue[ready_pids.index(pid_running)]
    vruntimes[pid_running] += 1 * (1.25**process['Priority'])
    return pid_running