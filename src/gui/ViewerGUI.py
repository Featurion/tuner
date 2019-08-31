from .QWindow import QWindow
from ..client.VideoManager import VideoManager


class ViewerGUI(QWindow):

    def __init__(self, title, cb):
        super().__init__()
        self.__cb = cb
        self.video_mgr = None
        self.setWindowTitle(title)

    def start(self):
        self.video_mgr = VideoManager(self, self.__cb)
        self.video_mgr.moveToThread(app.daemon)
        super().start()
