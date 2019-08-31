from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

from .QWindow import QWindow


class ChannelSelectGUI(QWindow):

    def __init__(self, cb):
        super().__init__()
        self.__guiCallback = cb

        self.resize(600, 400)

        self.addr = QLabel(self)
        self.addr.setText('Broadcast ID:')
        self.addr.move(170, 155)

        self.channel = QLineEdit(self)
        self.channel.move(290, 160)
        self.channel.resize(150, 20)
        self.channel.setText('')

        self.button = QPushButton('Start', self)
        self.button.move(290, 180)
        self.button.resize(70, 25)
        self.button.clicked.connect(self.__cb)

    def __cb(self):
        try:
            channel = int(self.channel.text())
        except ValueError:
            return

        self.__guiCallback(channel)
