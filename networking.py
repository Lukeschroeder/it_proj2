import time
import random
import socket as mysoc


class Server:
    def __init__(self, port):
        self.port = port
        self.socket = self.createsocket()
        self.activesocket = None

    # Returns an active server socket 
    def createsocket(self):
        try:
            serversocket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
            print '[S]: Server socket created'
        except mysoc.error as err:
            print '{} \n'.format("socket open error ",err)
        port = self.port
        host = mysoc.gethostname()
        server_binding=(host,port)
        serversocket.bind(server_binding)
        serversocket.listen(1)
        print '[S]: Server socket listening'
        return serversocket

    def accept(self):
        self.activesocket, addr = self.socket.accept()   
        print '[S]: Accepting connection: ', addr[0] 

    def settimeout(self, t):
        self.socket.settimeout(t)


    def close(self):
        print '[S]: Closing connection'
        self.socket.close()



class Client:
    def __init__(self):
        self.socket = self.createsocket()

    # Returns active client socket
    def createsocket(self):
        # Open client socket
        try:
            clientsocket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
            print '[C]: Client socket created'
        except mysoc.error as err:
            print '{} \n'.format("socket open error ",err)

        # Return active socket
        return clientsocket

    def connecttoserver(self, hostname, port):
         # Connect to the server at the port passed
        server_binding = (hostname, port)
        self.socket.connect(server_binding)

    def settimeout(self, t):
        self.socket.settimeout(t)

    def close(self):
        print '[C]: Closing connection'
        self.socket.close()

    
