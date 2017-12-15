import threading
import base64
import struct
import socket
import queue

from src.base import utils

class ReceiverAI(object):

    def __init__(self, provider):
        self.__provider = provider

        self.__socket, (self.__address, self.__port) = self.__provider.getSocket().accept()

        self.__inbox = queue.Queue()
        self.__outbox = queue.Queue()

        send = threading.Thread(target=self.send)
        send.start()

    def getSocket(self):
        return self.__socket

    def getInbox(self):
        return self.__inbox.get_nowait()

    def getOutbox(self):
        return self.__outbox.get_nowait()

    def send(self):
        while True:
            try:
                data = base64.b85encode(self.getOutbox().toJSON().encode())

                size = len(data)

                packedSize = struct.pack('I', socket.htonl(size))

                utils.send(self.getSocket(), packedSize, 4)
                utils.send(self.getSocket(), data, size)
            except queue.Empty:
                continue
            except Exception as e:
                print(e)
                continue