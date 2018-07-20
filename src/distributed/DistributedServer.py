from src.distributed.ConnectionRepository import ConnectionRepository
from src.distributed.Datagram import Datagram

from src.base.constants import *

class DistributedServer(ConnectionRepository):

    def __init__(self, ip, port):
        ConnectionRepository.__init__(self, ip, port)

    def ejectClient(self, message):
        datagram = Datagram()
        datagram.setMsgType(CLIENT_EJECT)
        datagram.setData(message)

        self.sendDatagram(datagram)

    def handleMsgType(self, msgType, data):
        if msgType == CLIENT_HELLO:
            serverVersion = data[0]
            if serverVersion != SERVER_VERSION:
                self.ejectClient("Wrong server version!")
                return

            datagram = Datagram()
            datagram.setMsgType(CLIENT_HELLO_RESP)

            self.sendDatagram(datagram)