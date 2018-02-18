class Channel(object):

    def __init__(self):
        self.__image = None

    def setImage(self, image):
        self.__image = image

    def getImage(self):
        return self.__image