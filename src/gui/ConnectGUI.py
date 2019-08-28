from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from .QWindow import QWindow
from ..client.BroadcasterRepository import BroadcasterRepository
from ..client.ReceiverRepository import ReceiverRepository


class ConnectGUI(QWindow):

    def __init__(self, cb):
        super().__init__()
        self.__cb = cb

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
        self.port.setText('7199')

        bc_button = QPushButton('Broadcaster', self)
        bc_button.move(200, 180)
        bc_button.resize(120, 30)
        bc_button.clicked.connect(self.__make_cb(BroadcasterRepository))

        rc_button = QPushButton('Receiver', self)
        rc_button.move(380, 180)
        rc_button.resize(120, 30)
        rc_button.clicked.connect(self.__make_cb(ReceiverRepository))

    def getAddress(self):
        try:
            return (self.host.text(), int(self.port.text()))
        except ValueError:
            return ('', 0)

    def __make_cb(self, cls):
        def callback():
            address = self.getAddress()        
            self.__cb(cls, *address)
        return callback
