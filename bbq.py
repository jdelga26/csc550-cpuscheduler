from collections import defaultdict

rr_queue = []
time_slice = 10
remaining_time = None
quantum_table = defaultdict(int)

def calc_time_slice(rr_queue):
    sorted_rr_queue = sorted(rr_queue, key=lambda x:x['Factor'])
    low = sorted_rr_queue[0]['Burst Time']
    high = sorted_rr_queue[-1]['Burst Time']
    return (low + high) // 2

def factor_analysis(process):
    return (.5 * process['Burst Time']) + (.25 * process['Arrival Time']) + (.25 * process['Priority'])

def schedule(ready_queue):
    global rr_queue
    global time_slice
    global remaining_time
    global quantum_table
    
    if not rr_queue:
        for process in ready_queue:
            process['Factor'] = factor_analysis(process)
        rr_queue = ready_queue
        time_slice = calc_time_slice(rr_queue)
        remaining_time = time_slice
    if rr_queue:
        to_add = [process for process in ready_queue if process not in rr_queue]
        if to_add:
            for process in to_add:
                process['Factor'] = factor_analysis(process)
            time_slice = calc_time_slice(rr_queue)
            rr_queue.extend(to_add)
        to_subtract = [process for process in rr_queue if process not in ready_queue]
        if to_subtract:
            rr_queue.remove(to_subtract[0])
            time_slice = calc_time_slice(rr_queue)
            remaining_time = time_slice * (2**quantum_table[rr_queue[0]['Process id']])

    if not remaining_time:
        if rr_queue[0]['Burst Time'] <= (time_slice / 2):
            remaining_time = (time_slice / 2)
        else:
            quantum_table[rr_queue[0]['Process id']] += 1
            remaining_time = time_slice * (2**quantum_table[rr_queue[1]['Process id']])
            rr_queue.append(rr_queue[0])
            del rr_queue[0]

    remaining_time -= 1
    return rr_queue[0]['Process id']