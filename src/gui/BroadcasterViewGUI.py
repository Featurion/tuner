from .QWindow import QWindow
from ..client.VideoManager import VideoManager


class BroadcasterViewGUI(QWindow):

    def __init__(self):
        super().__init__()
        self.video_mgr = None
        self.setWindowTitle('Broadcaster')

    def start(self):
        self.video_mgr = VideoManager(self)
        self.video_mgr.moveToThread(app.daemon)
        super().start()

    def exitView(self):
        conn.is_active = False

    def closeEvent(self, event):
        event.accept()
        conn.is_active = False
