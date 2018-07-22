import cv2
import numpy as np

from PyQt5.QtCore import Qt, QObject, QPoint, QSize
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QVBoxLayout, QWidget


class VideoManager(QObject):

    class _View(QWidget):

        def paintEvent(self, event):
            frame = self.parent().video_mgr.frame
            if not frame or frame.isNull():
                event.ignore()
                return
            else:
                event.accept()

            cur_size = self.size()
            painter = QPainter(self)
            painter.drawImage(QPoint(0, 0), frame)

            if cur_size != frame.size():
                self.parent().resize(frame.size())
                geom = self.parent().frameGeometry()
                center = app.desktop().screenGeometry().center()
                geom.moveCenter(center)
                self.parent().move(geom.topLeft())

    def __init__(self, window):
        super().__init__(None)
        self.__frame = None
        self.__view = VideoManager._View(window)
        layout = QVBoxLayout(self.__view)
        window.setCentralWidget(self.__view)

    @property
    def resolution(self) -> QSize:
        return self.__view.size()

    @property
    def width(self) -> int:
        return self.__view.width()

    @property
    def height(self) -> int:
        return self.__view.height()

    @property
    def frame(self) -> QImage:
        return self.__frame

    @frame.setter
    def frame(self, frame: np.ndarray):
        if frame is None:
            # create a random static frame
            data = np.random.randint(2, size=(self.height, self.width),
                                      dtype=np.uint8)
            data = np.tile(np.atleast_3d(data), 3)
            data *= 255
        else:
            data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, _ = data.shape
        self.__frame = QImage(data.data, width, height, data.strides[0],
                              QImage.Format_RGB888)
        self.__view.update()
