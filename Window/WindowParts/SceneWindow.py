import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Button import Button
from Window.Items.Label import Label
from Window.Items.LineEdit import LineEdit
from Window.Items.Slider import Slider
from Window.Items.Sprite import Sprite


class SceneWindow(QGraphicsView):
    deleteSignal = pyqtSignal(str)
    # clickSignal = pyqtSignal(list)

    def __init__(self):
        super(SceneWindow, self).__init__()
        # self.resize(300, 100)
        self.setFixedSize(500, 300)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        brush = QBrush(QColor(0, 210, 0))
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

    def getParentItem(self, parentUUID):
        parentItem = None
        if parentUUID:
            items = self.scene.items()
            for item in items:
                if item.UUID == parentUUID:
                    parentItem = item
                    break

        return parentItem

    """Slots"""
    # def focus(self, UUIDList):
    #     itemsList = self.scene.items()
    #     for item in itemsList:
    #         item.setSelected(False)
    #
    #     for UUID in UUIDList:
    #         for item in itemsList:
    #             if item.UUID == UUID:
    #                 item.setSelected(True)
    #                 break
    #
    #     self.update()

    def delete(self, deletedItemsUUIDList):
        sceneItemsList = self.scene.items()
        for UUID in deletedItemsUUIDList:
            for item in sceneItemsList:
                if item.UUID == UUID:
                    print(UUID)
                    self.scene.removeItem(item)
                    break

    def add(self, itemName, UUID, parentUUID):
        # 先找到父项
        parentItem = self.getParentItem(parentUUID)

        # 再生成相应的项
        item = None
        if itemName == 'Button':
            item = self.makeButton(UUID, parentItem)
        elif itemName == 'Label':
            item = self.makeLabel(UUID, parentItem)
        elif itemName == 'LineEdit':
            item = self.makeLineEdit(UUID, parentItem)
        elif itemName == 'Slider':
            item = self.makeSlider(UUID, parentItem)
        elif itemName == 'Sprite':
            item = self.makeSprite(UUID, parentItem)

        if not parentItem:
            self.scene.addItem(item)

    def makeButton(self, UUID, parentItem):
        button = Button(UUID, parentItem)
        button.deleteSignal.connect(lambda: self.deleteSignal.emit(button.UUID))
        return button

    def makeLabel(self, UUID, parentItem):
        label = Label(UUID, parentItem)
        label.deleteSignal.connect(lambda: self.deleteSignal.emit(label.UUID))
        return label

    def makeLineEdit(self, UUID, parentItem):
        lineEdit = LineEdit(UUID, parentItem)
        lineEdit.deleteSignal.connect(lambda: self.deleteSignal.emit(lineEdit.UUID))
        return lineEdit

    def makeSlider(self, UUID, parentItem):
        slider = Slider(UUID, parentItem)
        slider.deleteSignal.connect(lambda: self.deleteSignal.emit(slider.UUID))
        return slider

    def makeSprite(self, UUID, parentItem):
        sprite = Sprite(UUID, parentItem)
        sprite.deleteSignal.connect(lambda: self.deleteSignal.emit(sprite.UUID))
        return sprite

    """Events"""
    # mousePressEvent有个多选bug，所以改为用mouseReleaseEvent
    # def mousePressEvent(self, event):
    #     super(SceneWindow, self).mousePressEvent(event)
    #     # UUIDList = []
    #     # for item in self.scene.selectedItems():
    #     #     UUIDList.append(item.UUID)
    #     #
    #     # print(self.scene.items())
    #     # print(UUIDList)
    #     # if UUIDList:
    #     #     self.clickSignal.emit(UUIDList)
    #     for item in self.scene.items():
    #         if item.hasFocus():
    #             print(item)

    # def paintEvent(self, event):
    #     super(SceneWindow, self).paintEvent(event)

    def resizeEvent(self, event):
        super(SceneWindow, self).resizeEvent(event)
        self.scene.setSceneRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())