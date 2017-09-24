import socket
import sys,traceback
import logging

#logging.basicConfig(filename='example.log', level=logging.DEBUG)

try:
    # Connect
    #logging.warning("connecting")
    socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_.bind(('localhost', int(sys.argv[1]))) # This is where the port is selected
    socket_.listen(1)
    connection, _ = socket_.accept()

    # IO Functions
    def sendStringPipe(toBeSent):
        sys.stdout.write(toBeSent+'\n')
        sys.stdout.flush()
    def getStringPipe():
        str =  sys.stdin.readline().rstrip('\n')
        return(str)
    def sendStringSocket(toBeSent):
        global connection
        toBeSent += '\n'
        connection.sendall(bytes(toBeSent, 'ascii'))
    def getStringSocket():
        global connection
        newString = ""
        buffer = '\0'
        while True:
            buffer = connection.recv(1).decode('ascii')
            if buffer != '\n':
                newString += str(buffer)
            else:
                return newString

    while True:
        # Handle Init IO
        sendStringSocket(getStringPipe()) # Player ID
        sendStringSocket(getStringPipe()) # Map Dimensions
        sendStringSocket(getStringPipe()) # Productions
        sendStringSocket(getStringPipe()) # Starting Map
        sendStringPipe(getStringSocket()) # Player Name / Ready Response

        # Run Frame Loop
        while True:#for i in range(30):
            sendStringSocket(getStringPipe()) # Frame Map
            sendStringPipe(getStringSocket()) # Move List

except Exception as e:
    #logging.warning(traceback.format_exc())
    pass