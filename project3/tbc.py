import multiprocessing
import time
import os
import sys
from multiprocessing import Process
import socket
from queue import Queue
import random
import pika
import ssl

processArray = []
channelArray = []
pidArray = []
connection = pika.BlockingConnection(
    pika.ConnectionParameters("127.0.0.1", heartbeat=600)
)
number_of_processes = 0
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type="fanout")
BRAOADCAST = "broadcast"
UPDATE = "update"

class Process2(Process):
    def __init__(
        self,
        process_id,
        number_of_requests,
        min_time,
        max_time,
        average_time,
    ):
        Process.__init__(self)
        self.process_id = process_id
        self.timestampArr = []
        self.number_of_requests = number_of_requests
        self.min_time = min_time
        self.max_time = max_time
        self.average_time = average_time
        self.requestCount = 0
        self.receivedMessage = 0
        self.pendingRequest = []
        #create an array of number_of_processes and initilize it to 0
        self.timestampArr = [0] * number_of_processes
        channel.queue_bind(exchange="logs", queue=str(self.process_id))
        channel.queue_declare(queue=str(self.process_id))

    def helperBroadcast(self, message, pid):
        channel.basic_publish(exchange="logs", routing_key=str(pid), body=message)

    def createConnectionSend(self,message, pid):
        if message[0] == BRAOADCAST:
            self.timestampArr[self.process_id] += 1
            self.pendingRequest.append((message, message[3], self.process_id))
        else: #update message
            self.helperBroadcast(message, pid)
        channel.basic_publish(exchange="logs", routing_key=str(pid), body=message)
        print("Message is sent", message)

    def callback(self, ch, method, properties, body):
        if type == BRAOADCAST:
            pass
        message = (type, self.timestampArr[self.process_id], self.process_id)
        print(method.routing_key, "aaaaaaaaa")
        if method.routing_key != str(self.process_id):
            print(self.process_id, " [x] Received %r" % body)
            self.receivedMessage += number_of_processes
            if self.receivedMessage >= number_of_processes * (number_of_processes - 1):
                self.receivedMessage = 0
                if self.number_of_requests <= self.requestCount - 1:
                    print(
                        "Node "
                        + str(self.process_id)
                        + " sending request "
                        + str(self.number_of_requests)
                        + " at time "
                        + str(time.time())
                    )
                    if body[0] == BRAOADCAST:
                        self.timestampArr[body[3]] = body[2] 
                        self.pendingRequest.append((body, body[2], body[3]))
                        if body[2] > self.timestampArr[self.process_id]:
                            self.timestampArr[self.process_id] = body[2]
                            message = (UPDATE, self.timestampArr[self.process_id], self.process_id)
                            self.createConnectionSend(message, self.process_id)
                    else: #update message
                        self.timestampArr[body[3]] = body[2]
                    time.sleep(self.get_t())
                self.requestCount += 1
            if self.requestCount > self.number_of_requests:
                print(
                    "Node "
                    + str(self.process_id)
                    + " has completed "
                    + str(number_of_processes)
                    + " requests"
                )
                connection.close()

    def createConnectionReceive(self, queue_name):
        channel.basic_consume(
            queue=str(queue_name), auto_ack=True, on_message_callback=self.callback
        )

        channel.queue_bind(exchange="logs", queue=str(queue_name))
        channel.start_consuming()

    def run(self):
        while self.requestCount <= self.number_of_requests:
            self.createConnectionSend(self.process_id)
            self.requestCount += 1
            print("Process ", self.process_id, " sent request")
            self.createConnectionReceive(self.process_id)
            print(
                "Process ",
                self.process_id,
                " received request ",
            )


# generate ramdom t
def random_t_generator(average_time, min_time, max_time):
    t = random.expovariate(1.0 / average_time)
    while t < min_time or t > max_time:
        t = random.expovariate(1.0 / average_time)
    return t


def main():

    if len(sys.argv) != 6:
        print("tbc.py NP MINT, MAXT, AVGT, NR")
        sys.exit(1)
    else:
        # read 5 arguments from command line
        number_of_processes = int(sys.argv[1])
        if number_of_processes < 2 or number_of_processes > 20:
            print("Number of processes must be between 2 and 20")
            return

        min_time = int(sys.argv[2])
        if min_time < 0:
            print("Min time must be greater than 0")
            return
        max_time = int(sys.argv[3])
        if max_time > 60000:
            print("Max time must be less than 60000")
            return
        average_time = int(sys.argv[4])
        number_of_requests = int(sys.argv[5])
        print("Number of processes: ", number_of_processes)
        print("Min time: ", min_time)
        print("Max time: ", max_time)
        print("Average time: ", average_time)
        print("Number of requests: ", number_of_requests)

    # create number_of_processes processes
    for i in range(number_of_processes):
        p = Process2(
            i,
            number_of_requests,
            min_time,
            max_time,
            average_time,
        )

        random.seed(p.pid, time.time())
        random_t_generator(average_time, min_time, max_time)
        processArray.append(p)
        p.start()

    # wait for all processes to finish
    for p in processArray:
        p.join()


if __name__ == "__main__":
    main()
