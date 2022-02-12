import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Label import Label
from Window.Items.Sprite import Sprite


class SceneWindow(QGraphicsView):
    deleteSignal = pyqtSignal(str)

    def __init__(self):
        super(SceneWindow, self).__init__()
        # self.resize(300, 100)
        self.setFixedSize(500, 300)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        brush = QBrush(QColor(100, 100, 100))
        self.scene.setBackgroundBrush(brush)

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
    def add(self, itemName, UUID):
        print(itemName)
        if itemName == 'Label':
            self.addLabel(UUID)
        elif itemName == 'Sprite':
            self.addSprite(UUID)

    def addButton(self, UUID):
        ...

    def addLabel(self, UUID):
        label = Label(UUID)
        label.setHtml('Hello PyPlay')
        label.setHtml('Hello PyPlay')

        label.deleteSignal.connect(lambda: self.deleteSignal.emit(label.uuid))
        self.scene.addItem(label)

    def addLineEdit(self, UUID):
        ...

    def addSlider(self, UUID):
        ...

    def addSprite(self, UUID):
        sprite = Sprite(UUID)
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
        self.scene.setSceneRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())