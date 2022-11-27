import sys
import os
import socket
from multiprocessing import Process

# write a node class that will communicate with the sockets and the server
# and will be able to send and receive messages
TOKEN = "1"
REQUEST = "0"


# Socket Helper Functions

def sendToken(logFile, rightNode, pending_request, using):
    logFile.write("Sending token to " + str(rightNode) + "\n")
    using = False
    if(pending_request):
        tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tmp.connect(('localhost', rightNode))
        tmp.sendto(TOKEN.encode(), ("127.0.0.1", rightNode))
        pending_request = False
        
def sendRequest(logFile, leftNode):
    logFile.write("Sending request to " + str(leftNode) + "\n")
    tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp.connect(('localhost', leftNode))
    tmp.sendto(REQUEST.encode(), ("127.0.0.1", leftNode))
    print("Sent request to " + str(leftNode))
    tmp.close()
   
def recieve(sock, maxTime, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request):
    logFile.write("Waiting for data\n")
    data = sock.recvfrom(1024)
    logFile.write("Received raw data: " + str(data) + "\n")
    data = data[0].decode()
    logFile.write("Received data: " + str(data) + "\n")
    if(data == REQUEST):
        logFile.write("Received token from " + str(leftNode) + "\n")
        using = True
        sendToken(logFile, rightNode, pending_request, using)
    elif(data == TOKEN):
        hungry = True
        if(asked==False):
            sendRequest(logFile, leftNode)
            asked = True
       
        logFile.write("Received request from " + str(rightNode) + "\n")
        if(data == 0 and using == False):
            sendToken(logFile, rightNode, pending_request, using)
        else:
            pending_request = True
            if(asked == False and data == 1):
                sendRequest(logFile, leftNode)
                asked = True 
    else:
        asked = False
        if(hungry==True):
            using = True
            hungry = False
        else:
            sendToken(logFile, rightNode, pending_request, using)
            pending_request=False

# Socket Executable

def run(sock, maxTime, dataFile, delta, totalCnt, logFileName, rightNode, leftNode, hungry, using, asked, pending_request):
    logFile = open(logFileName, "a")
    # Initialize the data file
    dataFile = open(dataFile, "a")
    dataFile.write("0")

    logFile.write("Listening on port " + str(sock) + "\n")
    logFile.write("Max time " + str(maxTime) + "\n")
    logFile.write("Log file " + str(logFileName) + "\n")
    counter = 0
    print("Running")
    sockInstance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockInstance.bind(('localhost', sock))
    sendRequest(logFile, leftNode)
    while True:
        print("Waiting for data")
        recieve(sockInstance, maxTime, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request)
        counter = counter + 1
        print("Counter: " + str(counter))
        if(counter >= totalCnt):
            print("Closing")
            sockInstance.close()
            logFile.close()
            dataFile.close()
            break


# Main Executable
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
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000 + i)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        socketArray.append(server_address[1])
    
    # Print socket array

    for i in range(0, numOfProcess):
        if(i==0):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[i+1],socketArray[numOfProcess - 1], False, True, False, False)))
        elif(i==numOfProcess-1):
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[0], socketArray[i - 1], False, True, False, False)))
        else:
            nodeArray.append(Process(target=run, args=(socketArray[i], maxTime, inputFileName, delta, exitCount, logFileName, socketArray[i+1], socketArray[i - 1], False, True, False, False)))

    for i in range(0, len(nodeArray)):
        nodeArray[i].start()

# Run the main executable
if __name__ == "__main__":
    main()