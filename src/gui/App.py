from PyQt5.QtWidgets import QApplication

from ..gui.ConnectGUI import ConnectGUI


class App(QApplication):

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

        self.__window = window

        if self.window:
            self.window.start()

    def start(self):
        self.window = ConnectGUI(self.connect)
        self.exec_()

    def connect(self, host, port):
        pass

    def cleanup(self):
        pass
