# write a node class that will communicate with the sockets and the server
# and will be able to send and receive messages
import socket
import time
TOKEN = 1
REQUEST = 0
class Node:
    def __init__(self, dataFile, delta, totalCnt, logFileName, maxTime, sock, rightNode, leftNode, hungry, using, asked, pending_request):
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
        self.pending_request = pending_request
        self.logFile = open(logFileName, "w")
        self.logFile.write("Node started at " + time.strftime("%H:%M:%S") + "\n")

    
    def start(self):

        # Listen for incoming connections
        self.sock.listen(1)
        self.logFile.write("Listening on port " + str(self.sock) + "\n")
        self.logFile.write("Max time " + str(self.maxTime) + "\n")
        self.logFile.write("Log file " + str(self.logFileName) + "\n")
        self.logFile.write("")
        self.run()
    
   
    
    def sendToken(self):
        self.logFile.write("Sending token to " + str(self.rightNode) + "\n")
        msg = 1
        self.using = False
        if(self.pending_request):
            tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tmp.connect(('localhost', self.rightNode))
            tmp.sendto(msg.encode(), ("127.0.0.1", self.rightNode))
            self.pending_request = False


    def sendRequest(self):
        self.logFile.write("Sending request to " + str(self.leftNode) + "\n")
        msg = 0
        tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp.connect(('localhost', self.leftNode))
        tmp.sendto(msg.encode(), ("127.0.0.1", self.leftNode))
       
    
    def recieve(self):
        (conn, addr) = self.sock.accept()
        data = conn.recv(1024).decode()
        if(data == REQUEST):
            self.logFile.write("Received token from " + str(self.leftNode) + "\n")
            self.using = True
            self.sendToken()
        elif(data == TOKEN):
            self.hungry = True
            if(self.asked==False):
                self.sendRequest()
                self.asked = True
           
            self.logFile.write("Received request from " + str(self.rightNode) + "\n")
            if(data == 0 and self.using == False):
                self.sendToken()
            else:
                self.pending_request = True
                if(self.asked == False and data == 1):
                    self.sendRequest()
                    self.asked = True 
        else:
            self.asked = False
            if(self.hungry==True):
                self.using = True
                self.hungry = False
            else:
                self.sendToken()
                self.pending_request=False

        #conn.close()

        
    
    def close(self):
        self.logFile.write("Closing socket\n")
        self.sock.close()
    
    def run(self):
        counter = 0
        while True:
            self.recieve()
            counter += 1
            if(counter >= self.totalCnt):
                break
        self.close()
