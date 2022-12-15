class Queue:
    def __init__(self, number_of_processes, timestamp, process_id):
        self.queue = []
        self.number_of_processes = number_of_processes
        self.timestamp = timestamp
        self.process_id = process_id
        self.timestampIndex = 0

    # A process can remove the message from the request queue with the smallest timestamp, !,
    #  if it has received a message from every other process with timestamp greater than !.
    def enqueue(self, item):
        self.queue.append(item)
        self.timestampIndex += 1

    def dequeue(self):
        if self.isEligibleToRemove(self.process_id, self.timestamp):
            return self.queue.pop(self.timestampIndex)

    def isEligibleToRemove(self, process_id, timestamp):
        cmp = timestamp[process_id]
        cnt = 0
        for i in range(len(self.queue)):
            if cmp < self.queue[i][process_id]:
                cnt += 1

        return cnt == self.number_of_processes - 1

    def size(self):
        return len(self.queue)

    def __str__(self):
        return str(self.queue)
