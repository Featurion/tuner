import json

class Datagram(object):

    def __init__(self):
        self.__command = int()
        self.__data = None

    def getCommand(self):
        return self.__command

    def setCommand(self, command):
        self.__command = command

    def getData(self):
        return self.__data

    def setData(self, data):
        self.__data = data

    @staticmethod
    def fromJSON(str_):
        obj = json.loads(str_)

        datagram = Datagram()
        datagram.setCommand(obj['command'])
        datagram.setData(obj['data'])

        return datagram

    def toJSON(self):
        data = self.getData()

        return json.dumps({
            'command': self.getCommand(),
            'data': data,
        })