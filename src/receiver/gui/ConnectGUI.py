from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from src.gui.Window import Window
from src.receiver.gui.ViewerGUI import ViewerGUI


class ConnectGUI(Window):

    def __init__(self):
        super().__init__()

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
        self.port.setText('7199')

        self.button = QPushButton('Start', self)
        self.button.move(290, 180)
        self.button.resize(70, 25)
        self.button.clicked.connect(self.__connect)

    def __connect(self):
        host, port = self.host.text(), self.port.text()
        app.window = ViewerGUI(host, int(port))
