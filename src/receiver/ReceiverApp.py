from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication

from src.receiver.gui.ConnectGUI import ConnectGUI


class ReceiverApp(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])
        self.aboutToQuit.connect(self.cleanup)
        self.__window = None

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        if self.window:
            self.window.cleanup()
            self.window.close()

        self.__window = window

        if self.window:
            self.window.start()
            self.window.show()

    @pyqtSlot()
    def start(self):
        self.window = ConnectGUI()
        self.exec_()

    @pyqtSlot()
    def cleanup(self):
        if self.window:
            self.window = None
