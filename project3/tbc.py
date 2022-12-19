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
import datetime as dt

processArray = []
channelArray = []
pidArray = []
connection = pika.BlockingConnection(
    pika.ConnectionParameters("127.0.0.1", heartbeat=600)
)
connection.process_data_events()

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
        number_of_processes,
    ):
        Process.__init__(self)
        self.process_id = process_id
        self.timestampArr = []
        self.number_of_requests = number_of_requests
        self.number_of_processes = number_of_processes
        self.min_time = min_time
        self.max_time = max_time
        self.average_time = average_time
        self.requestCount = 0
        self.receivedMessage = 0
        self.pendingRequest = []

        # create an array of number_of_processes and initilize it to 0
        self.timestampArr = [0] * number_of_processes
        channel.queue_bind(exchange="logs", queue=str(self.process_id))
        channel.queue_declare(queue=str(self.process_id))

    def helperBroadcast(self, message, pid):
        encodedMsg = self.encode_msg(message)
        channel.basic_publish(
            exchange="logs", routing_key=str(pid), body=bytes(encodedMsg, "utf-8")
        )

    def helperPending(self, timestamp):
        val = not True
        for i in range(len(self.pendingRequest)):
            if self.pendingRequest[i][1] == timestamp:
                return i
        return val

    def encode_msg(self, tuple):
        return "" + tuple[0] + "," + str(tuple[1]) + "," + str(tuple[2])

    def decode_msg(self, message):
        a, b, c = tuple(message.decode("utf-8").split(","))
        return (a, int(b), int(c))

    def createConnectionSend(self, message, pid):
        encodedMsg = self.encode_msg(message)

        if message[0] == BRAOADCAST:
            self.timestampArr[self.process_id] += 1
            self.pendingRequest.append((message[0], message[1], self.process_id))
            self.pendingRequest.sort(key=lambda x: x[1])
        else:  # update message
            self.helperBroadcast(message, pid)

        while len(self.pendingRequest) > 0:
            publishItem = self.pendingRequest.pop(0)
            encodedPublishItem = self.encode_msg(publishItem)
            # open x.txt ile dosyayı açıp içine yazıyoruz
            with open("x.txt", "a") as f:
                f.write(
                    f"pid={str(self.process_id).zfill(2)}, ospid={os.getpid()}, reqid={str(publishItem[2]).zfill(4)}, ts={str(publishItem[1]).zfill(4)}:{str(self.process_id).zfill(2)}, rt={str(dt.datetime.fromtimestamp(time.time())).split( )[1]}\n"
                )
            print(
                "pid=",
                str(self.process_id).zfill(2),
                "ospid=",
                os.getpid(),
                "reqid=",
                str(publishItem[2]).zfill(4),
                "ts=",
                str(publishItem[1]).zfill(4),
                ":",
                str(self.process_id).zfill(2),
                "rt=",
                str(dt.datetime.fromtimestamp(time.time())).split()[1],
                "\n",
            )

            channel.basic_publish(
                exchange="logs",
                routing_key=str(pid),
                body=bytes(encodedPublishItem, "utf-8"),
            )

    def callback(self, ch, method, properties, body):
        # message = (type, self.timestampArr[self.process_id], self.process_id)
        if method.routing_key != str(self.process_id):
            decodedBody = self.decode_msg(body)
            self.receivedMessage += self.number_of_processes
            if self.receivedMessage >= self.number_of_processes * (
                self.number_of_processes - 1
            ):
                self.receivedMessage = 0
                # if self.number_of_requests <= self.requestCount - 1:
                if decodedBody[0] == BRAOADCAST:
                    self.timestampArr[decodedBody[2]] = decodedBody[1]
                    self.pendingRequest.append(
                        (decodedBody[0], decodedBody[1], decodedBody[2])
                    )
                    self.pendingRequest.sort(key=lambda x: x[1])

                    if decodedBody[1] > self.timestampArr[self.process_id]:
                        self.timestampArr[self.process_id] = decodedBody[1]
                        message = (
                            UPDATE,
                            self.timestampArr[self.process_id],
                            self.process_id,
                        )

                        self.createConnectionSend(message, self.process_id)

                    else:  # update message
                        self.timestampArr[decodedBody[2]] = decodedBody[1]

                    time.sleep(
                        random_t_generator(
                            self.average_time,
                            self.min_time / 1000,
                            self.max_time / 1000,
                        )
                    )

                    self.timestampArr[self.process_id] += 1
                    msg = (
                        BRAOADCAST,
                        self.timestampArr[self.process_id],
                        self.process_id,
                    )

                    self.createConnectionSend(msg, self.process_id)

                else:
                    self.timestampArr[decodedBody[2]] = decodedBody[1]
                self.requestCount += 1
            if self.requestCount > self.number_of_requests:

                connection.close()
                sys.exit()

    def createConnectionReceive(self, queue_name):
        channel.basic_consume(
            queue=str(queue_name), auto_ack=True, on_message_callback=self.callback
        )

        channel.queue_bind(exchange="logs", queue=str(queue_name))
        channel.start_consuming()

    def run(self):
        self.timestampArr[self.process_id] += 1
        msg = (BRAOADCAST, self.timestampArr[self.process_id], self.process_id)
        self.createConnectionSend(msg, self.process_id)
        # self.requestCount += 1

        self.createConnectionReceive(self.process_id)


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
        global number_of_processes
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
            number_of_processes,
        )

        random.seed(p.pid, time.time())
        random_t_generator(average_time, min_time, max_time)
        processArray.append(p)
        p.start()

    # wait for all processes to finish
    for p in processArray:
        p.join()


if __name__ == "__main__":
    f = open("x.txt", "w")
    main()
