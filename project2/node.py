# write a node class that will communicate with the sockets and the server
# and will be able to send and receive messages
from multiprocessing import Process
import random
import socket
import sys
import time
TOKEN = "1"
REQUEST = "0"

nodeArray = []
socketArray = []
processArray = []

class Node(Process):
    def __init__(self, dataFile, delta, totalCnt, updateCount, logFileName, maxTime, sock, rightNode, leftNode, hungry, using, asked, pending_request, holder, initialTime):
        super(Node, self).__init__()
        self.sock = sock
        self.maxTime = maxTime
        self.dataFile = dataFile
        self.delta = delta
        self.totalCnt = totalCnt
        self.logFileName = logFileName
        self.rightNode = rightNode
        self.leftNode = leftNode
        self.hungry = hungry
        self.using = using
        self.asked = asked
        self.holder = holder
        self.pending_request = pending_request
        self.updateCount = updateCount
        self.initialTime = initialTime 
        print("Node started at " + time.strftime("%H:%M:%S") + "\n")
    
    def sendToken(self):
        print("Sending token to " + str(self.rightNode) + "\n")
        msg = 1
        if(self.pending_request):
            tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tmp.sendto(msg.encode(), ("localhost", self.rightNode))
            self.pending_request = False


    def sendRequest(self):
        print("Sending request to " + str(self.leftNode) + "\n")
        msg = 0
        if self.updateCount < self.totalCnt:
            tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            tmp.sendto(msg.encode(), ("localhost", self.leftNode))

    def recieve(self):
        data = self.sock.recv(1024).decode()
        if(data == REQUEST):
            print("Received token from " + str(self.leftNode) + "\n")
            if self.holder and not self.using:
                self.sendToken()
            else:
                self.pending_request = True
                if self.holder == False and not self.asked:
                    self.sendRequest()
                    self.asked = True
        elif(data == TOKEN):
            print("Node " + str(self._pid) + " received token")
            self.holder = True
            self.asked = False
            if self.hungry:
                self.using = True
                self.hungry = False
            else:
                self.sendToken()
                self.pending_request = False
            
    def close(self):
        print("Closing socket\n")
        self.sock.close()
    
    def run(self):
        server_address = ('localhost', self.port)
        self.sock.bind(server_address)
        while self.totalUpdateCount < self.totcount:
            time.sleep(random.uniform(0, self.maxTime))
            if self.totalUpdateCount >= self.totcount:
                break
            if self.holder != True:
                self.hungry = True
                if not self.asked:
                    self.sendRequest("request")
                    self.asked = True
                if(self.totalUpdateCount < self.totcount):
                    self.receive()
            else:
                self.using = True
                self.updateDataFile()
                self.using = False
                self.hungry = False
                self.receive()
                if self.pending_requests:
                        self.sendToken("token")
                        self.holder = "other"
                        self.pending_requests = False
            print("Node " + str(self.index) + "closing")            
            self.close()


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

    for i in range(0, numOfProcess):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the port
        server_address = ('localhost', 10000 + i)
        sock.bind(server_address)
        socketArray.append(sock)
    # Create processes
    for i in range(0, numOfProcess):
        #ataFile, delta, totalCnt, updateCount, logFileName, maxTime, sock, rightNode, leftNode, hungry, using, asked, pending_request
        if i == 0:
            p = Process(target=Node, args=(dataFile, delta, 0, logFileName, maxTime, socketArray[i], socketArray[(i+1) % len(socketArray)], socketArray[(i-1) % len(socketArray)], False, False, False, False, True))
        else:
            p = Process(target=Node, args=(dataFile, delta, 0, logFileName, maxTime, socketArray[i], socketArray[i+1] % len(socketArray), socketArray[i-1] % len(socketArray), False, False, False, False, False))
        p.start()
        processArray.append(p)
    # Start all processes
    for i in range(0, len(nodeArray)):
        processArray[i].start()
    
    # Wait for all processes to finish
    for i in range(0, len(nodeArray)):
        processArray[i].join()

# Run the main executable
if __name__ == "__main__":
    main()