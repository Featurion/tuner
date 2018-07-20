from src.base.constants import *
from src.base.core import Datagram
from src.base.client import ClientRepository


class DistributedClient(ClientRepository):

    def sendHello(self):
        dg = Datagram()
        dg['code'] = CLIENT_HELLO
        dg['data'] = SERVER_VERSION
        self.sendDatagram(dg)

    def handleDatagram(self, dg):
        if dg['code'] == CLIENT_HELLO_RESP:
            pass
