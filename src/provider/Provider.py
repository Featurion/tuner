from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton


class Provider(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('Provider')
        self.resize(600, 400)

        self.addr = QLabel(self)
        self.addr.setText('Host/Port:')
        self.addr.move(220, 160)

        self.host = QLineEdit(self)
        self.host.move(290, 160)
        self.host.resize(100, 20)
        self.host.setText('127.0.0.1')

        self.port = QLineEdit(self)
        self.port.move(400, 160)
        self.port.resize(50, 20)
        self.port.setText('1613')

        button = QPushButton('Start', self)
        button.move(290, 180)


class ProviderUI(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])

    def start(self):
        self.__provider = Provider()
        self.__provider.show()
        self.exec_()
