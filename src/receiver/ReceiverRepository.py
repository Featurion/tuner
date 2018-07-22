import cv2

from src.network.ClientRepository import ClientRepository


class ReceiverRepository(ClientRepository):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__running = False

    @property
    def running(self):
        return self.__running

    def connect(self):
        self.__running = True
        super().connect()

    def disconnect(self):
        self.__running = False
