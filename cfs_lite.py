vruntimes = {}       # Keeps record of how much CPU time a process has used... Somewhat. This value is scaled by priority per process ("niceness"). Also new processes that show up for the first time aren't automatically owed a bunch of CPU time just because the device happens to have been running for a while.

target_latency = 100 # Can guarantee this latency on any process of average or above-average priority.
min_slice = 5        # Minimum number of ticks a process must be allowed to run before context switching.

pid_running = None   # Keep track of the currently running process.
time_elapsed = 0     # The currently running process will keep running until a certain amount of time elapses. How much time has to elapse depends on how many other processes are waiting their turn currently.

def schedule(ready_queue):
    global vruntimes
    global pid_running
    global time_elapsed

    ready_pids = [process['Process id'] for process in ready_queue]

    for pid in ready_pids:
        if pid not in vruntimes.keys():
            if len(vruntimes):
                vruntimes[pid] = min(vruntimes.values())
            else:
                vruntimes[pid] = 0.

    if pid_running in ready_pids and time_elapsed < max(target_latency // len(ready_queue), min_slice):
        process = ready_queue[ready_pids.index(pid_running)]
        vruntimes[pid_running] += 1 * (1.25**(-process['Priority']))
        time_elapsed += 1
        return pid_running

    pid_running = min(ready_pids, key=vruntimes.get)
    process = ready_queue[ready_pids.index(pid_running)]
    vruntimes[pid_running] += 1 * (1.25**(-process['Priority']))
    time_elapsed = 1
    return pid_running