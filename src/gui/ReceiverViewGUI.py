from .QWindow import QWindow
from .ChannelSelectGUI import ChannelSelectGUI
from ..client.VideoManager import VideoManager


class ReceiverViewGUI(QWindow):

    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.video_mgr = None
        self.setWindowTitle('Receiver')

    def start(self):
        self.video_mgr = VideoManager(self)
        self.video_mgr.moveToThread(app.daemon)
        conn._activate = self.channel
        super().start()

    def exitView(self):
        conn.is_active = False

    def closeEvent(self, event):
        event.accept()
        conn.is_active = False
