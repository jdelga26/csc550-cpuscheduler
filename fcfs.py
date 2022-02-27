def schedule(ready_queue):
    return min(ready_queue, key=lambda x:x['Arrival Time'])['Process id']
