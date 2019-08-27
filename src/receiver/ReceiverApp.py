from ..base.ClientAgent import ClientAgent
from ..gui.GraphicalApp import GraphicalApp
from ..gui.RemoteViewGUI import RemoteViewGUI
from ..receiver.ReceiverRepository import ReceiverRepository


class ReceiverApp(GraphicalApp):

    def __init__(self):
        super().__init__()
        self.is_viewing = False

    def connect(self, host, port):
        super().connect(ReceiverRepository, host, port)
        self.window = RemoteViewGUI()
        self.is_viewing = True

    def cleanup(self):
        self.is_viewing = False
        super().cleanup()
