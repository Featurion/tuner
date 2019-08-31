import uvloop

from PyQt5.QtCore import QThread

from ..network.ClientRepository import ClientRepository


class ClientAgent(QThread):

    def __init__(self, cls=ClientRepository):
        super().__init__()
        self.conn = None
        self.__cls = cls
        self.__address = None

    def start(self, host, port):
        self.__address = (host, port)
        super().start()

    def run(self):
        self.conn = self.__cls(*self.__address, loop=uvloop.new_event_loop())
        self.conn.setblocking(False)
        self.conn.run()

    def quit(self):
        if self.conn:
            self.conn.disconnect()
        super().quit()
