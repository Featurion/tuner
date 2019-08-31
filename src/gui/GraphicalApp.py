from PyQt5.QtWidgets import QApplication

from ..client.ClientAgent import ClientAgent
from ..gui.ConnectGUI import ConnectGUI


class GraphicalApp(QApplication):

    def __init__(self):
        QApplication.__init__(self, [])
        self.aboutToQuit.connect(self.cleanup)
        self.__window = None
        self.__net_thread = None

    @property
    def window(self):
        return self.__window

    @property
    def daemon(self):
        return self.__net_thread

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

    def connect(self, cls, host, port):
        try:
            self.__net_thread = ClientAgent(cls)
            self.__net_thread.start(host, int(port))
        except ValueError:
            pass

    def cleanup(self):
        if self.__net_thread:
            self.__net_thread.quit()
            self.__net_thread.wait()
            self.__net_thread = None

        self.window = None
