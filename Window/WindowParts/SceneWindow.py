import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Label import Label


class SceneWindow(QGraphicsView):
    def __init__(self):
        super(SceneWindow, self).__init__()
        # self.setBackgroundBrush(QBrush(QColor(100, 100, 100)))

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.scene.setSceneRect(2, 2, 100, 100)

        # self.pixmap = QPixmap('/Users/louis/Desktop/pyplay/res/d7e409bfa2ee4e3b956738ca1f6445e8.png')
        # self.pixmap = self.pixmap.scaled(self.width(), self.height())
        # self.brush = QBrush(pixmap)
        # self.scene.setBackgroundBrush(brush)

        label = QGraphicsTextItem()
        label.setHtml('123')
        # self.scene.addPixmap(pixmap)
        self.scene.addItem(label)

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()

    def initWindowAttrs(self):
        ...

    def initWidgets(self):
        ...

    def initSignals(self):
        ...

    """Slots"""
    def add(self, itemName):
        print(itemName)
        if itemName == 'Label':
            self.addLabel()

    def addLabel(self):
        label = Label()
        label.setHtml('Hello PyPlay')
        self.scene.addItem(label)

    def addSprite(self):
        ...

    """Events"""
    def paintEvent(self, event):
        super(SceneWindow, self).paintEvent(event)
        print(self.width())
        print(self.height())

        painter = QPainter(self.viewport())
        # painter.setBrush(self.brush)
        # painter.drawRect(0, 0, 100, 100)

        pixmap = QPixmap('/Users/louis/Desktop/pyplay/res/d7e409bfa2ee4e3b956738ca1f6445e8.png')
        painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())