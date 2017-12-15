from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton

from src.base import utils

from src.receiver.Receiver import Receiver

class ReceiverUI(QApplication):
    startReceiverSignal = pyqtSignal(str, int)
    resetSignal = pyqtSignal()

    def __init__(self):
        QApplication.__init__(self, [])

        self.startReceiverSignal.connect(self.__startReceiver)
        self.resetSignal.connect(self.reset)

        self.__receiverThread = QThread()
        self.__receiverThread.start()

        self.__resolution = self.desktop().screenGeometry()
        self.__width = self.__resolution.width()
        self.__height = self.__resolution.height()

        self.__window = None
        self.__receiver = None

    def getReceiverThread(self):
        return self.__receiverThread

    def getResolution(self):
        return (self.__width, self.__height)

    def getSize(self):
        width, height = self.getResolution()
        return QSize(width, height)

    @pyqtSlot()
    def start(self):
        self.__window = Window(self)
        self.__window.show()

        self.exec_()

    def reset(self):
        del self.__window
        del self.__receiver

        self.__window = None
        self.__receiver = None

        self.__window = Window(self)
        self.__window.show()

    @pyqtSlot(str, int)
    def __startReceiver(self, ip, port):
        del self.__window
        self.__window = None

        self.__receiver = Receiver(self, ip, port)

class Window(QMainWindow):

    def __init__(self, ui):
        QMainWindow.__init__(self)

        self.__ui = ui

        self.setWindowTitle("Receiver")
        self.resize(600, 400)

        self.ipport = QLabel(self)
        self.ipport.setText("IP/Port:")
        self.ipport.move(250, 155)

        self.ip = QLineEdit(self)
        self.ip.move(290, 160)
        self.ip.resize(100, 20)
        self.ip.setText("127.0.0.1")

        self.port = QLineEdit(self)
        self.port.move(400, 160)
        self.port.resize(50, 20)
        self.port.setText("1613")

        self.button = QPushButton('Start', self)
        self.button.move(290, 180)
        self.button.resize(70, 25)
        self.button.clicked.connect(self.start)

    def start(self):
        ip = self.ip.text()
        port = self.port.text()

        try:
            port = int(port)
        except ValueError:
            print('Invalid port!')
            return

        self.__ui.startReceiverSignal.emit(ip, port)