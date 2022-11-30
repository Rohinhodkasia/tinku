import socket
import threading
import time


def server():
    localIP = "0.0.0.0"
    localPort = 48003
    bufferSize = 4096
    msgFromServer = "Response from server"
    bytesToSend = str.encode(msgFromServer)
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    print("UDP server up and listening")


    # client()
    # serverAddressPort = ("0.0.0.0", 48002)
    # UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # print("\nUDPClientSocket Response : ", UDPClientSocket)
    # ParamReq = {0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x09}
    # ConfigReq = '{0x01, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x01, 0x09}'
    # RunReq = "{0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00}"
    # msg = [ParamReq, ConfigReq, RunReq]
    # for m in msg:
    #     mess = str.encode(m)
    #     print(mess)
    #     UDPClientSocket.sendto(m, serverAddressPort)
    #     time.sleep(100)

    while True:
        print("\n Waiting for new meassage .....")
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]
        # clientMsg = "Message from Client:{}".format(message)
        # clientIP = "Client IP Address:{}".format(address)
        # print(clientMsg)
        # print(clientIP)
        # UDPServerSocket.sendto(bytesToSend, address)

        # msg = "Message from Server {}".format(msgFromServer[0])
        print("Message from RANV :", bytesAddressPair)


def client():
    # msgFromClient = "Hello UDP Server"
    # bytesToSend = str.encode(msgFromClient)
    serverAddressPort = ("0.0.0.0", 48002)
    # bufferSize = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    print("\nUDPClientSocket Response : ", UDPClientSocket)
    a = UDPClientSocket.connect(serverAddressPort)

    ParamReq = [0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x09]
    ConfigReq = [0x01, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x01, 0x09]
    RunReq = [0x01, 0x01, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]
    msg = [ParamReq, ConfigReq, RunReq]
    for m in msg:
        #mess = str.encode(m)
        print(m)
        UDPClientSocket.sendto(bytearray(m), serverAddressPort)
        time.sleep(10)

    # print("Sending msg to server: ", bytesToSend)
    # UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    #
    # msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    #
    # msg = "Message from Server {}".format(msgFromServer[0])
    #
    # print(msg)


if __name__ == '__main__':
    t1 = threading.Thread(name="server", target=server).start()
    client()
