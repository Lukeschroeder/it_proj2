import sys
import socket
infilename = 'PROJI-DNSRS.txt'
DNStable = {}
TS_hostname = None
from networking import Server, Client
datalength = 200


lsListenPort = None
ts1Hostname = None
ts1ListenPort = None
ts2Hostname = None
ts2ListenPort = None


def contactTSservers(server, ts1client, ts2client):

    ts1client.connecttoserver(ts1Hostname, ts1ListenPort)
    ts2client.connecttoserver(ts2Hostname, ts2ListenPort)

    while(True):
        hostname = server.activesocket.recv(datalength)
        if len(hostname) == 0: break
        ts1client.socket.send(hostname)
        ts2client.socket.send(hostname)
        ts1client.settimeout(5.0)
        ts2client.settimeout(5.0)

        try:
            response = ts1client.socket.recv(datalength).decode('utf-8')
            if len(response) > 0:
                server.activesocket.send(response.encode('utf-8'))
        except socket.timeout:
            try:
                response = ts2client.socket.recv(datalength).decode('utf-8')
                if len(response) > 0:   
                    server.activesocket.send(response.encode('utf-8'))
            except socket.timeout:
                response = hostname + ' - Error:HOST NOT FOUND'
                server.activesocket.send(response.encode('utf-8'))

        


def main():
    # print command line arguments
    args = sys.argv

    if len(args) != 6: print 'Insufficient Arguments'

    global lsListenPort
    global ts1Hostname
    global ts1ListenPort
    global ts2Hostname
    global ts2ListenPort


    lsListenPort = int(args[1])
    ts1Hostname = args[2]
    ts1ListenPort = int(args[3])
    ts2Hostname = args[4]
    ts2ListenPort = int(args[5])

    server = Server(lsListenPort)
    ts1client = Client()
    ts2client = Client()

    server.accept()
    contactTSservers(server, ts1client, ts2client)
    server.close()



if __name__ == "__main__":
    main()