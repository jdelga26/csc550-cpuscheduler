def simulate(workload):
    t = 0
    while len(workload) > 0:
        for i, process in enumerate(workload):
            if process["Arrival Time"] > t:
                ready_queue = workload[:i]
                break
        i = schedule(ready_queue)
        print(workload[i])
        workload[i]["Burst Time"] -= 1

        if(workload[i]["Burst Time"] == 0):
            del workload[i]
        t += 1

def schedule(ready_queue):
    return ready_queue.index(min(ready_queue, key=lambda x:x['Arrival Time']))
