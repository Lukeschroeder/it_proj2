import sys
import socket
infilename = 'PROJI-DNSRS.txt'
DNStable = {}
TS_hostname = None
from networking import Server, Client
from threading import Thread, Event
datalength = 200
import time

lsListenPort = None
ts1Hostname = None
ts1ListenPort = None
ts2Hostname = None
ts2ListenPort = None

response = ''



def readresponse(client, hostname, e):
    global response 

    client.settimeout(5.0)
    try:
        response = client.socket.recv(datalength).decode('utf-8')
        e.set()
    except socket.timeout:
        if response == '':
            response = hostname + ' - Error:HOST NOT FOUND'
            e.set()




def contactTSservers(server, ts1client, ts2client):
    global response
    global threads

    ts1client.connecttoserver(ts1Hostname, ts1ListenPort)
    ts2client.connecttoserver(ts2Hostname, ts2ListenPort)
    e = Event()


    while(True):
        hostname = server.activesocket.recv(datalength)
        if len(hostname) == 0: break

        response = ''
        threads = []
        

        ts1client.socket.send(hostname)
        ts2client.socket.send(hostname)

        threads.append(Thread(target=readresponse, args=(ts1client, hostname, e)))
        threads.append(Thread(target=readresponse, args=(ts2client, hostname, e)))

        tic = time.time()
        threads[0].start()
        threads[1].start()
        e.wait()
        e.clear()
        toc = time.time()

        print 'Hostname: ' + hostname + ' Time: ' + str(round(toc - tic, 5)) + '(s)'

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