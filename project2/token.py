import sys
import os
import socket
from node import Node

def main():

    # Check for correct number of command line arguments
    if len(sys.argv) != 7:
        print("Usage: python token.py <host> <port> <host> <port> <host> <port>")
        sys.exit(1)

    # Get the input file name
    numOfProcess = int(sys.argv[1])
    if (numOfProcess < 2 or numOfProcess > 20):
        print("Number of processes must be between 2 and 20")
        return
    # Get the input file name
    inputFileName = sys.argv[2]
    # Get increment delta
    delta = int(sys.argv[3])
    if delta < 0:
        print("Delta must be greater than 0")
        return
    # Get exit count
    exitCount = int(sys.argv[4])
    # Get log file name
    logFileName = sys.argv[5]
    # Get max time
    maxTime = int(sys.argv[6])

    # Create a TCP/IP socket
    nodeArray = []
    socketArray = []
    for i in range(0, numOfProcess):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000 + i)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        socketArray.append(server_address[1])

    for i in range(0, numOfProcess):
        if(i==0):
            nodeArray.append(Node(sock=sock, maxTime=maxTime, dataFile=inputFileName, delta=delta, totalCnt=exitCount, logFileName=logFileName, rightNode=socketArray[i+1],leftNode=socketArray[numOfProcess - 1], hungry=False, using=True, asked=False,pending_request= False))
        elif(i==numOfProcess-1):
            nodeArray.append(Node(sock=sock, maxTime=maxTime, dataFile=inputFileName, delta=delta, totalCnt=exitCount, logFileName=logFileName, rightNode=socketArray[0],leftNode=socketArray[i - 1], hungry=False, using=True, asked=False,pending_request= False))
        else:
            nodeArray.append(Node(sock=sock, maxTime=maxTime, dataFile=inputFileName, delta=delta, totalCnt=exitCount, logFileName=logFileName, rightNode=socketArray[i+1],leftNode=socketArray[i - 1], hungry=False, using=True, asked=False,pending_request= False))

    for i in range(0, len(nodeArray)):
        # Create n child processes
        pid = os.fork()
        if pid == 0:
            # Child process
            nodeArray[i].start()
            break
    for i in range(0, len(socketArray)):
        # Close the socket
        socketArray[i].close()

main()