## TCP client for sending generic commands

import sys
import struct
import socket

## default TCP IP address and port#
# TCP_IP = '172.20.10.8'
TCP_IP = '10.0.0.101'
TCP_PORT = '8888'


## Simple text menu
def printMenu():
    print("\n")
    print (30 * "-","MENU", 30 * "-")
    print ("Enter CMD# followed by n Parameters")
    print("separated by :" )
    print (" ")
    print ("SEND to send messages to Feather")
    print ("CLEAR to clear command list")
    print ("EXIT to exit TCP Client")
    print (67 * "-")

def createFormatString():
    formatStringList = ["<b"] ## elimate paiing with <, big little endian fomrat!
    for i in cmdList:
        cmdSplit = i.split(':')
        formatStringList.append("bb")
        for j in range(len(cmdSplit)-1):
            formatStringList.append("i")
    baseString = "".join(formatStringList)
    return baseString
    print ("The data format is: " + baseString)

def printCmdList():
    for i in cmdList:
        print (i)
    ## createFormatString()

def sendTCP(fString):
    dataValues = []
    print("Sending Data over TCP")
    BUFFER_SIZE = 256
    dataValues.append(len(cmdList)) ## This is the number of commands being sent
    for i in cmdList:
        print("i: " + i)
        ## dataValues.append 1st element, byte cmd value
        ## abc = i.splint(':')
        ## for j in range(1..len(abc))
        cmdSequence = i.split(':')
        dataValues.append(int(cmdSequence[0])) ## covert to byte or int here
        dataValues.append(len(cmdSequence)-1)
        ##for j in i.split(':'):
        for j, val in enumerate(cmdSequence):
            print("j: " + str(j) + " value: " + str(val))
            if (j > 0):
                dataValues.append(int(val))
    print("the formatString is: " + fString)
    print(str(dataValues))
    dataPkr = struct.Struct(fString)
    pkd_data = dataPkr.pack(*dataValues)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, 8888))
    s.sendall(pkd_data)
    data = s.recv(BUFFER_SIZE)
    s.close()

cmdList = []
## dataValues = []
formatString = "b" ## always start with a byte that represents the number of cmds to be sent
loop = True

while loop:
    printMenu()
    userInput=input("Enter your menu selection:")
    if userInput.lower() == 'exit':
        print("Exiting TCP Client")
        exit()
    elif userInput.lower() == 'send':
        print("Send commands to feather")
        printCmdList()
        ##print(createFormatString())
        sendTCP(createFormatString())
    elif userInput.lower() == 'clear':
        cmdList = []
    else:
        cmdList.append(userInput)
