from base64 import b85encode, b85decode
from msgpack import loads, dumps

class Datagram(object):

    def __init__(self, predata=None):
        object.__init__(self)

        self.__msgType = 0
        self.__data = None

        if predata:
            self.load(predata)

    def getMsgType(self):
        return self.__msgType

    def setMsgType(self, msgType):
        self.__msgType = msgType

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data

    def load(self, data):
        obj = loads(b85decode(data))

        self.setMsgType(obj['msgType'])
        self.setData(obj['data'])

    def pack(self):
        data = self.getData()
        msgType = self.getMsgType()

        return b85encode(dumps({
            'msgType': msgType,
            'data': data
        }))