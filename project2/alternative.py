import sys
import os
import socket
from multiprocessing import Process

# write a node class that will communicate with the sockets and the server
# and will be able to send and receive messages
TOKEN = "1"
REQUEST = "0"

nodeArray = []
socketArray = []

def sendToken(logFile, rightNode, pending_request):
    if(pending_request):
        tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp.sendto(TOKEN.encode(), ("127.0.0.1", rightNode))
        pending_request = False
                
def sendRequest(leftNode):
    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp.sendto(REQUEST.encode(), ("127.0.0.1", leftNode))

def recieve(sock, maxTime, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request, holder):
    
    # If dataFile line 2 is more than or equal to totalCnt, close the socket and exit
    tmpCheck = open(dataFile, "r")
    data = tmpCheck.readlines()
    print("data: ",data)
    tmpCheck.close()
    if int(data[1]) >= totalCnt:
        sock.close()
        return
    if hungry:
        if(holder):
            asked = False
            using = True
            hungry = False
            # Access the critical section
            data[0] = int(data[0]) + delta
            data[1] = int(data[1]) + 1
            data = str(data[0]) + "\n" + str(data[1])
            dataFile = open(dataFile, "w")
            dataFile.write(str(data))
            dataFile.close()
            if pending_request:
                using = False
                sendToken(logFile, rightNode, pending_request)
                pending_request=False
                holder = False
        else:
            hungry = True
            if not asked:
                sendRequest(leftNode)
                asked = True

    msg = sock.recvfrom(1024)
    msg = msg[0].decode()

    if(str(msg) == REQUEST):
        if holder and not using:
            sendToken(logFile, rightNode, pending_request)
            holder = False
        else:
            pending_request = True
            if not holder and not asked:
                sendRequest(leftNode)
                asked = True      
    elif(str(msg) == TOKEN):
        asked = False
        if hungry:
            using = True
            hungry = False
            # Access the critical section
            asked = False
            using = True
            hungry = False
            # Access the critical section
            data[0] = int(data[0]) + delta
            data[1] = int(data[1]) + 1
            data = str(data[0]) + "\n" + str(data[1])
            dataFile = open(dataFile, "w")
            dataFile.write(str(data))
            dataFile.close()
            if pending_request:
                using = False
                sendToken(logFile, rightNode, pending_request)
                pending_request=False
                holder = False

# Socket Executable
def run(sock, maxTime, dataFile, delta, totalCnt, logFileName, rightNode, leftNode, hungry, using, asked, pending_request, holder):
    logFile = open(logFileName, "a")
    logFile.write("Listening on port " + str(sock) + "\n")
    logFile.write("Max time " + str(maxTime) + "\n")
    logFile.write("Log file " + str(logFileName) + "\n")
    counter = 0
    sockInstance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockInstance.bind(('localhost', sock))
    while True:
        recieve(sockInstance, maxTime, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request, holder)
        counter = counter + 1
        
        tmpCheck = open(dataFile, "r")
        data = tmpCheck.readlines()
        print("run data: ",data)
        print("totalCnt ",totalCnt)
        tmpCheck.close()
        if int(data[1]) >= totalCnt:
            return

# Main Executable
def main():

    # Check for correct number of command line arguments
    if len(sys.argv) != 7:
        print("Usage: python token.py <NP> <DATAFILE> <DELTA> <TOTCOUNT> <LOGFILE> <MAXTIME>")
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

    # Initialize the log file
    logFile = open(logFileName, "w")
    # Clear the log file
    logFile.write("")
    logFile.close()
    # Initialize the data file
    dataFile = open(inputFileName, "w")
    dataFile.write("0\n0")
    dataFile.close()
    # Create TCP/IP sockets
    for i in range(0, numOfProcess):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000 + i)
        sock.bind(server_address)

        socketArray.append(server_address[1])
    # Create processes
    for i in range(0, numOfProcess):
        if(i==0):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[i+1],socketArray[numOfProcess - 1], True, True, False, True, True)))
        elif(i==numOfProcess-1):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[0], socketArray[i - 1], True, False, False, False, False)))
        else:
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[i+1], socketArray[i - 1], True, False, False, False, False)))
    # Start all processes
    for i in range(0, len(nodeArray)):
        nodeArray[i].start()

# Run the main executable
if __name__ == "__main__":
    main()