import socket
import sys
import os
import base64
import threading
import time
import logging
from ast import literal_eval


# To create log files of the Conversation between UEV and Minku
logging.basicConfig(filename="Minkulogs.txt",
                    level=logging.DEBUG,
                    format='%(levelname)s: %(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    )

#### To over write oneclickLog.txt
handler = logging.FileHandler("Minkulogs.txt", 'w+')

# function to create socket and bind with /tmp/uev
def prep():
    srv_sock = '/tmp/uev'
    try:
        os.unlink(srv_sock)
    except:
        if os.path.exists(srv_sock):
            raise
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        print('Setting up server socket on %s\n' % srv_sock)
        sock.bind(srv_sock)
        sock.listen(1)
        print('Success, listening on unix domain socket %s\n' % srv_sock)
        return sock
    except Exception as e:
        print(e)
        return False


# Server function to accept connection
def server():
    print("main")
    sock = prep()
    print("before if")
    if not sock:
        return False
    while True:
        connection, client = sock.accept()
        print("\nConnection: ", connection, "\n Client : ", client)
        time.sleep(5)
        try:
            buffer = ''
            rcvd_bytes = 0
            while True:
                time.sleep(.5)
                data = connection.recv(1024)
                rcvd_bytes = rcvd_bytes + len(data)
                if not data:
                    print('waiting for receiving data.....\n')

                else:

                    buffer = buffer.encode() + data
                    print("\n Msg From MINTU Received at UEV : ", data)
                    logging.info("MSG from MINTU Received at UEV: {}".format(data))

        finally:
            print('Closing the connection\n')
            connection.close()
            print('Connection closed\n')


# Function to receive message from socket while connected and print received messages from the UEV
def recv_msg_from_uev(sock):
    while True:
        print("while client")
        data1 = sock.recv(4096)
        print('\nReceiving from UEV at MINTU : ', data1, "/n")
        logging.info("Response from UEV at MINTU: {}".format(data1))


# Function to create client socket and connect with server_address and send messages to UEV
def client():
    server_address = '/tmp/uev'
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    #  sock=prep()
    print('connecting to %s' % server_address)

    #    try:
    socketobj = ""
    sock.connect(server_address)
    socketobj = [sock]
    print("\n SOCKET OBJECT : ", socketobj)
    # CsendData(sock)
    t1 = threading.Thread(name="recv_msg_from_uev", target=recv_msg_from_uev, args=socketobj).start()
    time.sleep(0.01)
    CsendData(sock)


def CsendData(sock):
    msg0 = [0x0]
    msg10 = [0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4, 0x00, 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0x01, 0x00,
             0x00, 0xa0]
    msg11 = [0x02, 0x00, 0x00, 0x00, 0x93, 0x00, 0x06, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00]
    msg12 = [0x01, 0x00, 0x00, 0x00, 0xec, 0x03, 0x0a, 0x00, 0x04, 0x00, 0x00, 0x00, 0x53, 0x1f, 0x55, 0x1f]
    msg = [msg0, msg10, msg11, msg12]

    for message in msg:
        print("\Sending Data to UE : ", message)
        sock.sendall(bytearray(message))
        logging.info("Sending Messages to UEV: {}".format(message))
        time.sleep(4)


client()
