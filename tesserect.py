import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QWidget, QTextBrowser, QDialog

import pyscreenshot
import pytesseract


class MyWidgets(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_MacNoShadow)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()


    def paintEvent(self, event):

        # Draw rectangle
        qp = QPainter()
        qp.begin(self)
        x, y, w, h = self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()
        qp.drawLine(0, 0, 0, h)
        qp.drawLine(0, h-1, w-1, h-1)
        qp.drawLine(w-1, h-1, w-1, 0)
        qp.end()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            im = self.grabRectImage()
            text = pytesseract.image_to_string(im)
            self.showText(text)


    def showText(self, text):
        t = TextWindow()
        t.setText(text)
        t.exec_()


    def grabRectImage(self):
        x, y, w, h = self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()
        return pyscreenshot.grab(bbox=(x, y, x + w, y + h))


class TextWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.txt = QTextBrowser(self)
        self.layout = QGridLayout()
        self.layout.addWidget(self.txt)
        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def setText(self, text):
        self.txt.setText(text)
        self.txt.adjustSize()
        self.adjustSize()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MyWidgets()

    sys.exit(app.exec_())
