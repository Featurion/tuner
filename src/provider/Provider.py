import socket
import struct
import base64
import queue
import threading

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton

from src.base import constants, utils

from src.base.Datagram import Datagram
from src.provider.ReceiverAI import ReceiverAI

class Provider(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Provider")
        self.resize(600, 400)

        self.ipport = QLabel(self)
        self.ipport.setText("IP/Port:")
        self.ipport.move(250, 160)

        self.ip = QLineEdit(self)
        self.ip.move(290, 160)
        self.ip.resize(100, 20)
        self.ip.setText("127.0.0.1")

        self.port = QLineEdit(self)
        self.port.move(400, 160)
        self.port.resize(50, 20)
        self.port.setText("1613")

        button = QPushButton('Start server', self)
        button.move(290, 180)
        button.clicked.connect(self.startServer)

    def getSocket(self):
        return self.__socket

    def getInbox(self):
        return self.__inbox.get_nowait()

    def getOutbox(self):
        return self.__outbox.get_nowait()

    def receiveDatagram(self, datagram):
        self.__inbox.put(datagram)

    def sendDatagram(self, datagram):
        self.__outbox.put(datagram)

    def startServer(self):
        ip = self.ip.text()
        port = self.port.text()

        try:
            port = int(port)
        except ValueError:
            print('Invalid port!')
            return

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__socket.bind((ip, port))
        self.__socket.listen(0)

        self.__inbox = queue.Queue()
        self.__outbox = queue.Queue()

        wait = threading.Thread(target=self.wait)
        wait.start()

    """
    TODO: Broadcaster

    def recv(self):
        while True:
            try:
                sizeSignal = utils.recv(self.getSocket(), 4)
                size = socket.ntohl(struct.unpack('I', sizeSignal)[0])
                data = utils.recv(self.getSocket(), size)

                data = base64.b85decode(data)

                datagram = Datagram.fromJSON(data)
                self.handleReceiverDatagram(datagram)
            except struct.error as e:
                print(str(e))
                print('connection was closed unexpectedly')
                break
            except Exception as e:
                print(e)
                break

    def handleReceiverDatagram(self, datagram):
        print(datagram)
    """

    def wait(self):
        while True:
            try:
                ai = ReceiverAI(self)
            except Exception as e:
                print(e)

class ProviderUI(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])

    def start(self):
        self.__provider = Provider()
        self.__provider.show()

        self.exec_()