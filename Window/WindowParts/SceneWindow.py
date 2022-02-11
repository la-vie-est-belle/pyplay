import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Label import Label
from Window.Items.Sprite import Sprite


class SceneWindow(QGraphicsView):
    def __init__(self):
        super(SceneWindow, self).__init__()
        # self.resize(300, 100)
        self.setFixedSize(500, 300)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        brush = QBrush(QColor(100, 100, 100))
        self.scene.setBackgroundBrush(brush)

        label = Label()
        label.setHtml('11111111111')
        self.scene.addItem(label)

        label2 = Label()
        label2.setHtml('2222222')
        self.scene.addItem(label2)
        label2.setPos(20, 20)

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
        elif itemName == 'Sprite':
            self.addSprite()

    def addLabel(self):
        label = Label()
        label.setHtml('Hello PyPlay')
        self.scene.addItem(label)

    def addSprite(self):
        print(11111)
        sprite = Sprite()
        sprite.setPixmap(QPixmap('/Users/louis/Desktop/pyplay/res/d7e409bfa2ee4e3b956738ca1f6445e8.png'))
        self.scene.addItem(sprite)

    """Events"""
    def paintEvent(self, event):
        super(SceneWindow, self).paintEvent(event)
        # print(self.width())
        # print(self.height())
        #
        # painter = QPainter(self.viewport())
        # # painter.setBrush(self.brush)
        # # painter.drawRect(0, 0, 100, 100)
        #
        # pixmap = QPixmap('/Users/louis/Desktop/pyplay/res/d7e409bfa2ee4e3b956738ca1f6445e8.png')
        # painter.drawPixmap(0, 0, self.width(), self.height(), pixmap)
        # self.update()
        ...

    def resizeEvent(self, event):
        super(SceneWindow, self).resizeEvent(event)

        print(self.width())
        print(self.height())
        self.scene.setSceneRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())