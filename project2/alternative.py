import sys
import os
import time
import random
import socket
from multiprocessing import Process

# write a node class that will communicate with the sockets and the server
# and will be able to send and receive messages
TOKEN = "1"
REQUEST = "0"

nodeArray = []
socketArray = []

def accessResource(dataFileName, logFileName, initialTime, index, totalCnt, updateCnt, delta):
    # Open the data file and read the data
    dataFile = open(dataFileName, "r")
    # Read the data line by line
    data = dataFile.readlines()
    dataFile.close()
    # increment data[0] by delta
    data[0] = (int(data[0]) + delta)
    # increment data[1] by 1
    data[1] = (int(data[1]) + 1)

    # Access the critical section
    # Log file
    logFile = open(logFileName, "a")
    # Time in microseconds
    lctime = int(round(time.time() * 1000000)) - initialTime
    logFile.write("t=" + str(lctime) + ", pid=" + str(index) + ", os-pid=" + str(os.getpid()) + ", new="+ str(data[0])  + ", totalcount=" + str(totalCnt) + ", count=" + str(updateCnt) + "\n")
    data = str(data[0]) + "\n" + str(data[1])
    # Data file
    dataFile = open(dataFileName, "w")
    dataFile.write(str(data))
    dataFile.close()
    logFile.close()

def sendToken(rightNode):

    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp.sendto(TOKEN.encode(), ("127.0.0.1", rightNode))
                
def sendRequest(leftNode):
    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp.sendto(REQUEST.encode(), ("127.0.0.1", leftNode))

def dataFileCheck(dataFile, totalCnt):
    df = open(dataFile, "r")
    data = df.readlines()
    # Split the data
    data = data[1]
    if int(data) >= totalCnt - 1:
        return True
    return False

def recieve(sock, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request, holder, index, initialTime):

    # Recieve a message
    msg = sock.recv(1024).decode()
    print("Process ", index, " recieved ", msg)
    if(msg == TOKEN):
        print("Process ", index, " recieved token")
        holder = True
        asked = False
        if hungry:
            using = True
            hungry = False
        else:
            sendToken(rightNode)
            print("Process ", index, " sent token to ", rightNode)
            pending_request = False
    else:
        print("Process ", index, " recieved request")
        if holder and not using:
            sendToken(rightNode)
            print("Process ", index, " sent token to ", rightNode)
        else:
            pending_request = True
            if holder == False and not asked:
                sendRequest(leftNode)
                print("Process ", index, " sent request to ", leftNode)
                asked = True
    return hungry, using, asked, pending_request, holder

# Socket Executable
def run(sock, maxTime, dataFile, delta, totalCnt, logFileName, leftNode, rightNode, hungry, using, asked, pending_request, holder, index, initialTime, maxNode):
    sockInstance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockInstance.bind(("localhost", sock))
    updateCnt = 0
    print("Process ", index, " started")

    while updateCnt < totalCnt:
        if dataFileCheck(dataFile, totalCnt):
            break
        time.sleep(random.uniform(0, maxTime)/1000)
        if updateCnt >= totalCnt:
            break
        if not holder:
            hungry = True
            if not asked:
                sendRequest(leftNode)
                asked = True
            if updateCnt < totalCnt:
                hungry, using, asked, pending_request, holder = recieve(sockInstance, dataFile, delta, totalCnt, logFileName, rightNode, leftNode, hungry, using, asked, pending_request, holder, index, initialTime)
        else:
            using = True
            accessResource(dataFile, logFileName, initialTime, index, totalCnt, updateCnt, delta)
            updateCnt += 1
            using = False
            hungry = False
            try: 
                sockInstance.settimeout(maxTime * maxNode / 1000)
                hungry, using, asked, pending_request, holder = recieve(sockInstance, dataFile, delta, totalCnt, logFileName, rightNode, leftNode, hungry, using, asked, pending_request, holder, index, initialTime)
            except socket.timeout:
                hungry = False
                using = False
            if(pending_request):
                sendToken(rightNode)
                pending_request = False
                holder = False
    sockInstance.close()
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
    # Initial time in microseconds
    initialTime = int(round(time.time() * 1000000))
    # Create TCP/IP sockets
    for i in range(0, numOfProcess):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000 + i)
        sock.bind(server_address)

        socketArray.append(server_address[1])
    # Create processes
    for i in range(0, numOfProcess):
        if(i == 0):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[numOfProcess - 1],socketArray[1], True, True, False, True, True, i, initialTime, numOfProcess)))
            print("i =",i)
        elif(i == numOfProcess - 1):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[numOfProcess - 2], socketArray[0], True, False, False, False, False, i, initialTime, numOfProcess)))
            print("i =",i)
        else:
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[i - 1], socketArray[i + 1], True, False, False, False, False, i, initialTime, numOfProcess)))
            print("i =",i)
    # Start all processes
    for i in range(0, len(nodeArray)):
        print("Starting process ", i)
        nodeArray[i].start()

# Run the main executable
if __name__ == "__main__":
    main()