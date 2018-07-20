from socket import socket, AF_INET, SOCK_STREAM
from socket import ntohl, SOL_SOCKET, SO_REUSEADDR

from src.base.Datagram import Datagram
from src.base import utils

from threading import Thread
from queue import Queue, Empty

import struct

class ConnectionRepository(socket):

    def __init__(self, ip, port, type_=AF_INET, proto=SOCK_STREAM):
        socket.__init__(self, type_, proto)

        self.ip = ip
        self.port = port

        self.__inbox = Queue()

    def setIp(self, ip):
        self.ip = ip

    def getIp(self):
        return self.ip

    def setPort(self, port):
        self.port = port

    def getPort(self):
        return self.port

    def connect(self):
        result = socket.connect_ex(self, (self.getIp(), self.getPort()))

        self.setblocking(0)

        if result:
            self.handleConnect()
        else:
            print(str(result))

    def handleConnect(self):
        """
        Override
        """

        self.setupThreads()

    def sendThread(self):
        while True:
            try:
                data = self.__inbox.get_nowait()
                size = len(data)

                packedSize = struct.pack('I', htonl(size))

                utils.send(self, packedSize, 4)
                utils.send(self, data, size)
            except Empty:
                continue
            except struct.error:
                continue

    def sendDatagram(self, datagram):
        self.__inbox.put(datagram.pack())

    def receiveDatagram(self):
        while True:
            sizeSignal = utils.recv(self, 4)

            try:
                size = ntohl(struct.unpack('I', sizeSignal)[0])
            except struct.error:
                continue

            data = utils.recv(self, size)

            self.handleDatagram(data)

    def handleDatagram(self, data):
        datagram = Datagram(data)

        msgType = datagram.getMsgType()
        data = datagram.getData()

        self.handleMsgType(msgType, data)

    def handleMsgType(self, msgType, data):
        """
        Override
        """

    def setupThreads(self):
        self.receiveThread = Thread(target=self.receiveDatagram).start()
        self.sendThread = Thread(target=self.sendThread).start()

    def listen(self):
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        self.bind((self.getIp(), self.getPort()))
        socket.listen(self, 0)

        self.setupThreads()