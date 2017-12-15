import socket
import struct
import base64
import threading
import cv2
import numpy as np
import queue

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtCore import QObject, QPoint
from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtGui import QImage, QPainter

from src.base import constants, utils

from src.base.Datagram import Datagram

class ShowVideo(QObject):
    imageSignal = pyqtSignal(QImage)
    doVideoSignal = pyqtSignal()

    def __init__(self, ui, resolution, socket_ = None):
        super(ShowVideo, self).__init__(None)

        self.doVideoSignal.connect(self.__doVideo)

        self.__ui = ui
        self.__width, self.__height = resolution
        self.__socket = socket_
        self.__vrecv = queue.Queue()

    def getUI(self):
        return self.__ui

    def getSocket(self):
        return self.__socket

    def getInbox(self):
        return self.__inbox.get_nowait()

    def getOutbox(self):
        return self.__outbox.get_nowait()

    def receiveDatagram(self, datagram):
        self.__inbox.put(datagram)

    def sendDatagram(self, datagram):
        self.__outbox.put(datagram)

    def getResp(self):
        while True:
            if self.__resp:
                break

        resp = self.__resp
        self.__resp = None
        return resp

    def getRecv(self):
        return self.__vrecv.get_nowait()

    def __putRecv(self, recv):
        self.__vrecv.put(recv)

    @pyqtSlot()
    def startTransceiver(self):
        self.__inbox = queue.Queue()
        self.__outbox = queue.Queue()
        self.__channel = 0

        recv = threading.Thread(target=self.__recv, daemon=True)
        handler = threading.Thread(target=self.__handleDatagram, daemon=True)

        recv.start()
        handler.start()

        self.doVideoSignal.emit()

        #datagram = Datagram()
        #datagram.setCommand(constants.CHANGE_CH)
        #datagram.setData((self.__channel))

        #self.sendDatagram(datagram)

    @pyqtSlot()
    def __doVideo(self):
        video = cv2.VideoCapture(0)
        override = False
        set_ = True

        while True:
            try:
                recv = self.getRecv()
                override = False
            except queue.Empty:
                recv = None
            except Exception as e:
                print(e)
                override = True
                recv = None

            if not recv:
                if not set_:
                    video = cv2.VideoCapture("resources/static.mp4")
                    set_ = True
                ret, image = video.read()
                if isinstance(image, type(None)):
                    set_ = False
                    continue
            else:
                image = recv

            if override:
                image = np.zeros((self.__height, self.__width, 3), np.uint8)

            colorSwappedImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            height, width, _ = colorSwappedImage.shape

            image = QImage(colorSwappedImage.data,
                                    width,
                                    height,
                                    colorSwappedImage.strides[0],
                                    QImage.Format_RGB888)

            self.imageSignal.emit(image)

    def __handleDatagram(self):
        override = False

        while True:
            try:
                recv = self.getInbox()
            except queue.Empty:
                recv = None
            except Exception as e:
                print(e)
                recv = None

            if not recv:
                self.__putRecv(recv)
                return

            data = recv.getData()[self.__channel]

            if recv.getCommand() == constants.VIDEO_RELAY:
                self.__putRecv(data)

    def __recv(self):
        while True:
            try:
                sizeSignal = utils.recv(self.getSocket(), 4)
                size = socket.ntohl(struct.unpack('I', sizeSignal)[0])
                data = utils.recv(self.getSocket(), size)

                data = base64.b85decode(data)

                datagram = Datagram.fromJSON(data)
                self.receiveDatagram(datagram)
            except struct.error as e:
                continue
            except Exception as e:
                print(e)
                break

class ImageViewer(QWidget):

    def __init__(self, parent, size):
        super(ImageViewer, self).__init__(parent)

        self.image = QImage()
        self.size = size
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(QPoint(0, 0), self.image)
        self.image = QImage()

    @pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        self.setFixedSize(self.size)
        self.update()

class Receiver(QMainWindow):
    startTransceiver = pyqtSignal()

    def __init__(self, ui, ip, port):
        QMainWindow.__init__(self)

        self.__ui = ui

        self.__ip = ip
        self.__port = port

        self.connect()

    def getSocket(self):
        try:
            return self.__socket
        except AttributeError:
            pass

    def getUI(self):
        return self.__ui

    def connect(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__ip, self.__port))
        except Exception as e:
            print(e)
            self.__ui.resetSignal.emit()
            return

        self.__socket.setblocking(0)

        self.start()

    def start(self):
        self.setWindowTitle('Receiver')

        vid = ShowVideo(self.getUI(), self.getUI().getResolution(), self.getSocket())
        vid.moveToThread(self.getUI().getReceiverThread())

        imageViewer = ImageViewer(self, self.getUI().getSize())

        vid.imageSignal.connect(imageViewer.setImage)

        self.startTransceiver.connect(vid.startTransceiver)
        self.startTransceiver.emit()

        self.setCentralWidget(imageViewer)

        self.show()

        self.getUI().exec_()
