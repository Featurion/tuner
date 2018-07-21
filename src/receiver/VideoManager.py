import cv2
import numpy as np

from PyQt5.QtCore import Qt, QObject, QPoint, QSize
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QWidget


class VideoManager(QObject):

    class _View(QWidget):

        def __init__(self, mgr):
            super().__init__(app.window)
            app.window.setCentralWidget(self)
            self.__mgr = mgr

        def paintEvent(self, event):
            if self.__mgr.frame.isNull():
                event.ignore()
            else:
                event.accept()
                painter = QPainter(self)
                painter.drawImage(QPoint(0, 0), self.__mgr.frame)

    def __init__(self):
        super().__init__(None)
        self.__res = app.desktop().screenGeometry()
        self.__view = VideoManager._View(self)
        self.__view.setFixedSize(QSize(*self.resolution))
        self.__frame = QImage()

    @property
    def width(self) -> int:
        return self.__res.width()

    @property
    def height(self) -> int:
        return self.__res.height()

    @property
    def resolution(self) -> tuple:
        return (self.width, self.height)

    @property
    def frame(self) -> QImage:
        return self.__frame

    @frame.setter
    def frame(self, frame: np.ndarray):
        if frame is None:
            data = np.random.randint(2, size=(self.height, self.width),
                                      dtype=np.uint8)
            data = np.tile(np.atleast_3d(data), 3)
            data *= 255
        else:
            data = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.__frame = QImage(data.data, *self.resolution, data.strides[0],
                              QImage.Format_RGB888)
        self.__view.update()
