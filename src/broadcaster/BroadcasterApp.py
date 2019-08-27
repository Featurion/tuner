from ..gui.GraphicalApp import GraphicalApp
from ..gui.RemoteViewGUI import RemoteViewGUI
from ..broadcaster.BroadcasterRepository import BroadcasterRepository


class BroadcasterApp(GraphicalApp):

    def connect(self, host, port):
        super().connect(BroadcasterRepository, host, port)
