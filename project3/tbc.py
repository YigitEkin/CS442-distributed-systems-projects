import multiprocessing
import time
import os
import sys
from multiprocessing import Process
import socket
from queue import Queue
import random


process_list = []
socket_list = []


def Process():
    pass

# read 5 arguments from command line


def main():
    if len(sys.argv) != 6:
        print("tbc.py NP MINT, MAXT, AVGT, NR")
        sys.exit(1)
    else:
        number_of_processes = int(sys.argv[1])
        if number_of_processes < 2 or number_of_processes > 20:
            print("Number of processes must be between 2 and 20")
            return
        min_time = int(sys.argv[2])
        max_time = int(sys.argv[3])
        average_time = int(sys.argv[4])
        number_of_requests = int(sys.argv[5])
        print("Number of processes: ", number_of_processes)
        print("Min time: ", min_time)
        print("Max time: ", max_time)
        print("Average time: ", average_time)
        print("Number of requests: ", number_of_requests)

    # create number_of_processes processes
    for i in range(number_of_processes):

        # generate random time
        t = random.expovariate(1.0 / average_time)
        if t < min_time or t > max_time:
            t = random.uniform(min_time, max_time)

        p = Process(target=Process, args=(
            i, number_of_requests, min_time, max_time, average_time))
        process_list.append(p)
        p.start()

    # wait for all processes to finish
    for p in process_list:
        p.join()


main()
