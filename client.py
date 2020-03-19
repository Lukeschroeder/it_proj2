import sys
from networking import Client
infilename = 'PROJ2-HNS.txt'
outfilename = 'RESOLVED.txt'
datalength = 200
lsHostname = None
lsListenPort = None


def queryHostNames(lsclient):
    global lsHostname
    global lsListenPort

    # Open file of hostnames to query
    infile = open(infilename, 'r')
    outfile = open(outfilename, 'w+')
    lines = infile.readlines()

    lsclient.connecttoserver(lsHostname, lsListenPort)

    for index in range(len(lines)):
        hostname = lines[index].strip()
        request = hostname.lower().encode('utf-8')
        print '[C]: RS request: ', request
        lsclient.socket.send(request)
        response = lsclient.socket.recv(datalength).decode('utf-8')
        print 'RESPONSE: ', response

        if index != len(lines) - 1:
            outfile.write(response + '\n')
        else:
            outfile.write(response)

    lsclient.close()



def main():
    args = sys.argv
    if len(args) != 3: print 'Insufficient Arguments'

    global lsHostname
    global lsListenPort

    lsHostname = args[1]
    lsListenPort = int(args[2])

    lsclient = Client()

    queryHostNames(lsclient)




if __name__ == "__main__":
    main()
