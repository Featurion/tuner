from src.distributed.ConnectionRepository import ConnectionRepository
from src.distributed.Datagram import Datagram

from src.base.constants import *

class DistributedClient(ConnectionRepository):

    def __init__(self, ip, port):
        ConnectionRepository.__init__(self, ip, port)

    def sendHello(self):
        datagram = Datagram()
        datagram.setMsgType(CLIENT_HELLO)
        datagram.setData((SERVER_VERSION))

        self.sendDatagram(datagram)

    def handleMsgType(self, msgType, data):
        if msgType == CLIENT_HELLO_RESP:
            pass