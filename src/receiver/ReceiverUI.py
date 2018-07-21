from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton

from src.receiver.Receiver import Receiver


class ReceiverUI(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])
        self.__resolution = self.desktop().screenGeometry()
        self.__window = None

    @property
    def width(self):
        return self.__resolution.width()

    @property
    def height(self):
        return self.__resolution.height()

    @property
    def size(self):
        return QSize(self.width, self.height)

    @pyqtSlot()
    def start(self):
        self.__window = Window(self)
        self.__window.show()
        self.exec_()

    def reset(self):
        del self.__window
        self.__window = None
        self.__window = Window(self)
        self.__window.show()


class Window(QMainWindow):

    def __init__(self, ui):
        QMainWindow.__init__(self)

        self.__ui = ui

        self.setWindowTitle('Receiver')
        self.resize(600, 400)

        self.addr = QLabel(self)
        self.addr.setText('Host/Port:')
        self.addr.move(220, 155)

        self.host = QLineEdit(self)
        self.host.move(290, 160)
        self.host.resize(100, 20)
        self.host.setText('127.0.0.1')

        self.port = QLineEdit(self)
        self.port.move(400, 160)
        self.port.resize(50, 20)
        self.port.setText('1613')

        self.button = QPushButton('Start', self)
        self.button.move(290, 180)
        self.button.resize(70, 25)
        self.button.clicked.connect(self.start)

    def start(self):
        host = self.host.text()
        port = self.port.text()

        try:
            port = int(port)
        except ValueError:
            print('Invalid port!')
            return
