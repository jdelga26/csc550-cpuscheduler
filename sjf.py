def schedule(ready_queue):
    return min(ready_queue, key=lambda x:x['Burst Time'])['Process id']