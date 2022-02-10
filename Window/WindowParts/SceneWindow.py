import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Label import Label


class SceneWindow(QGraphicsView):
    def __init__(self):
        super(SceneWindow, self).__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())