
from threading import Thread
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtWidgets, uic
import sys
import cv2

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('camera.ui', self)
        self.openButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.closeButton = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.closeButton.setEnabled(False)
        self.cam = self.findChild(QtWidgets.QLabel, 'label')
        self.cam.setStyleSheet("background-image: url(cam.jpg)")
        self.openButton.clicked.connect(self.openButtonPressed)
        self.closeButton.clicked.connect(self.closeButtonPressed)
        self.oc = 0
        self.show()

    def videostream(self):
        self.vc = cv2.VideoCapture(0)
        while self.oc:

            try:
                rval, cap = self.vc.read()
                cap = cv2.cvtColor(cap, cv2.COLOR_BGR2RGB)
                image = QImage(cap, cap.shape[1], cap.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.cam.setPixmap(pixmap)
                self.show()
            except:
                print("error")
                continue
        self.vc.release()
        self.cam.clear()



    def openButtonPressed(self):
        self.oc = 1
        self.openButton.setEnabled(False)
        self.closeButton.setEnabled(True)
        self.thread = Thread(target=self.videostream, args=())
        self.thread.start()

    def closeButtonPressed(self):
        self.oc = 0
        self.closeButton.setEnabled(False)
        self.openButton.setEnabled(True)
        self.cam.setStyleSheet("background-image: url(cam.jpg)")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
