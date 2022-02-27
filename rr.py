time_slice = 10
next_task = None
current_task = None
remaining_time = None

def schedule(ready_queue):
    global next_task
    global current_task
    global remaining_time

    ready_ids = [process['Process id'] for process in ready_queue]

    if remaining_time == 0:
        current_task = None

    if current_task in ready_ids and remaining_time:
        if next_task is None and len(ready_queue) > 1:
            try:
                next_task = ready_ids[ready_ids.index(current_task) + 1]
            except IndexError:
                next_task = ready_ids[0]
        remaining_time -= 1
        return current_task
    else:
        remaining_time = time_slice - 1

        if next_task is None:
            current_task = ready_ids[0]
            if len(ready_ids) > 1:
                next_task = ready_ids[1]
            return ready_ids[0]
        else:
            current_task = next_task
            try:
                next_task = ready_ids[ready_ids.index(current_task) + 1]
            except IndexError:
                next_task = ready_ids[0]
            return current_task
        