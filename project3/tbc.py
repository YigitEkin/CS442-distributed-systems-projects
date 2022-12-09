import multiprocessing
import time
import os
import sys
from multiprocessing import Process
def Process():
    pass


#read 5 arguments from command line
def main():
    if len(sys.argv) != 6:
        print("tbc.py NP MINT, MAXT, AVGT, NR")
        sys.exit(1)
    else:
        number_of_processes = int(sys.argv[1])
        min_time = int(sys.argv[2])
        max_time = int(sys.argv[3])
        average_time = int(sys.argv[4])
        number_of_requests = int(sys.argv[5])
        print("Number of processes: ", number_of_processes)
        print("Min time: ", min_time)
        print("Max time: ", max_time)
        print("Average time: ", average_time)
        print("Number of requests: ", number_of_requests)

main()