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
connection = pika.BlockingConnection(pika.ConnectionParameters("127.0.0.1"))
# message = "hello"
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type="fanout")


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
        self.number_of_requests = number_of_requests
        self.min_time = min_time
        self.max_time = max_time
        self.average_time = average_time
        self.requestCount = 0

    def createConnectionSend(self, message, pid):
        channel.queue_declare(queue=str(pid))
        channel.queue_bind(exchange="logs", queue=str(pid))
        channel.basic_publish(exchange="logs", routing_key=str(pid), body=message)
        print("Message is sent", message)

    def callback(self, ch, method, properties, body):
        message = str(self.process_id)
        if method.routing_key != str(self.process_id):
            self.createConnectionSend(message, self.process_id)
            self.requestCount += 1
            if self.requestCount == self.number_of_requests:
                connection.close()
            print(self.process_id, " [x] Received %r" % body)

    def createConnectionReceive(self, queue_name):
        channel.queue_declare(queue=str(queue_name))
        channel.basic_consume(
            queue=str(queue_name), auto_ack=True, on_message_callback=self.callback
        )

        channel.queue_bind(exchange="logs", queue=str(queue_name))
        channel.start_consuming()

    def run(self):
        message = str(self.process_id)
        self.createConnectionSend(message, self.process_id)
        self.requestCount += 1
        print("Process ", self.process_id, " sent request ", message)
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
