def recieve(sock, maxTime, dataFile, delta, totalCnt, logFile, rightNode, leftNode, hungry, using, asked, pending_request):
    print("Waiting for data\n")
    data = sock.recvfrom(1024)
    print("Received raw data: " + str(data) + "\n")
    data = data[0].decode()
    print("Received data: " + str(data) + "\n")
    if(str(data) == TOKEN):
        logFile.write("Received token from " + str(leftNode) + "\n")
        using = True

        sendToken(logFile, rightNode, pending_request, using)
    elif(str(data) == REQUEST):
        hungry = True
        if(asked==False):
            sendRequest(logFile, leftNode)
            asked = True
       
        logFile.write("Received request from " + str(rightNode) + "\n")
        if(str(data) == REQUEST and using == False):
            sendToken(logFile, rightNode, pending_request, using)
        else:
            pending_request = True
            if(asked == False and str(data) == TOKEN):
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
