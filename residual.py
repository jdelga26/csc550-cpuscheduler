from audioop import reverse

rr_queue = []
time_slice = 10
remaining_time = time_slice

def schedule(ready_queue):
    global rr_queue
    global remaining_time

    if not rr_queue:
        rr_queue = sorted(ready_queue, key=lambda x:x['Burst Time'])
    if rr_queue:
        to_add = [process for process in ready_queue if process not in rr_queue]
        if to_add:
            for process in to_add:
                index = 0
                while index < len(rr_queue) and process['Burst Time'] >= rr_queue[index]['Burst Time']:
                    index += 1
                rr_queue = rr_queue[:index] + [process] + rr_queue[index:]
                if index == 0:
                    remaining_time = time_slice
        to_subtract = [process for process in rr_queue if process not in ready_queue]
        if to_subtract:
            rr_queue.remove(to_subtract[0])
            remaining_time = time_slice

    if not remaining_time:
        if rr_queue[0]['Burst Time'] <= time_slice:
            remaining_time = time_slice
        else:
            remaining_time = time_slice
            rr_queue.append(rr_queue[0])
            del rr_queue[0]

    remaining_time -= 1
    return rr_queue[0]['Process id']