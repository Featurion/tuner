from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from .Window import Window


class ConnectGUI(Window):

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

        self.button = QPushButton('Start', self)
        self.button.move(290, 180)
        self.button.resize(70, 25)
        self.button.clicked.connect(self.__cb_sanitized)

    def __cb_sanitized(self):
        try:
            host, port = self.host.text(), int(self.port.text())
        except ValueError:
            return

        self.__cb(host, port)
