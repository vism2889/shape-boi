import socket

class UDPListener():
    def __init__(self, msg):
        self.msg = msg
        self.localIP     = "127.0.0.1"
        self.localPort   = 20001
        self.bufferSize  = 1024
        self.msgFromServer       = "Hello UDP Client"
        self.bytesToSend         = str.encode(self.msgFromServer)
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


    def udpConnect(self):
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        print("UDP server up and listening")
        while(True):
            self.bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            self.message = self.bytesAddressPair[0]
            self.address = self.bytesAddressPair[1]
            self.msg = self.message.decode()
            self.clientIP  = "Client IP Address:{}".format(self.address)
            print('server listened message from client: ', self.msg)
            #self.handleMessage(clientMsg, currX, currY)
            '''
            print(clientMsg[:].split(',')[0])
            #print(clientIP)
            cx = int(clientMsg[:].split(',')[0])
            self.shape.setX(-cx//2)
            cy = int(clientMsg[:].split(',')[1])
            self.shape.setY(-cy//2)
            '''
            # Sending a reply to client
            self.UDPServerSocket.sendto(self.bytesToSend, self.address)
