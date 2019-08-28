from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QAbstractButton


class QImageButton(QAbstractButton):

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
