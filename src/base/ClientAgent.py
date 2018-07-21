import uvloop

from PyQt5.QtCore import QThread

from src.network.ClientRepository import ClientRepository


class ClientAgent(QThread):

    def __init__(self, host, port):
        super().__init__()
        self.__address = (host, port)

    def run(self):
        self.repo = ClientRepository(*self.__address,
                                     loop=uvloop.new_event_loop())
        self.repo.setblocking(False)
        self.repo.run()

    def quit(self):
        if self.repo._isRunning:
            self.repo._isRunning = False
        super().quit()
