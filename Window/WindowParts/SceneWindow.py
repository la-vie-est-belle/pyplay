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
    showPropertyWindowSignal = pyqtSignal(dict)
    clickSignal = pyqtSignal(list)

    def __init__(self):
        super(SceneWindow, self).__init__()
        # self.resize(300, 100)
        self.setFixedSize(500, 300)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        brush = QBrush(QColor(0, 210, 0))
        self.scene.setBackgroundBrush(brush)

        self.isCtrlPressed = False
        self.selectedItems = []

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

    def getItemByUUID(self, UUID):
        for item in self.scene.items():
            if item.UUID == UUID:
                return item

    """Slots"""
    def currentScene(self):
        return self.scene

    def showPropertyWindow(self, UUID):
        item = self.getItemByUUID(UUID)
        if item:
            propertyDict = item.getProperties()
            self.showPropertyWindowSignal.emit(propertyDict)

    def updateItemPropertiesOnScene(self, propertyDict):
        item = self.getItemByUUID(propertyDict['UUID'])
        if item:
            item.setProperties(propertyDict)

    def focus(self, UUIDList):
        itemsList = self.scene.items()
        for item in itemsList:
            item.setSelected(False)

        for UUID in UUIDList:
            for item in itemsList:
                if item.UUID == UUID:
                    item.setSelected(True)
                    break

        self.update()

    def delete(self, deletedItemsUUIDList):
        sceneItemsList = self.scene.items()
        for UUID in deletedItemsUUIDList:
            for item in sceneItemsList:
                if item.UUID == UUID:
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
        label.deleteSignal.connect(self.deleteSignal.emit)
        return label

    def makeLineEdit(self, UUID, parentItem):
        lineEdit = LineEdit(UUID, parentItem)
        lineEdit.deleteSignal.connect(lambda: self.deleteSignal.emit(lineEdit.UUID))
        return lineEdit

    def makeSlider(self, UUID, parentItem):
        slider = Slider(UUID, parentItem)
        slider.deleteSignal.connect(self.deleteSignal.emit)
        return slider

    def makeSprite(self, UUID, parentItem):
        sprite = Sprite(UUID, parentItem)
        sprite.deleteSignal.connect(lambda: self.deleteSignal.emit(sprite.UUID))
        return sprite

    """Events"""
    def mousePressEvent(self, event):
        super(SceneWindow, self).mousePressEvent(event)

        for item in self.scene.items():
            item.setSelected(False)

        item = self.scene.itemAt(event.pos(), QTransform())
        UUIDList = []
        if item:
            if self.isCtrlPressed:
                self.selectedItems.append(item)
            else:
                self.selectedItems = [item]

            for item in self.selectedItems:
                item.setSelected(True)
                UUIDList.append(item.UUID)
                
        self.clickSignal.emit(UUIDList)

    def mouseReleaseEvent(self, event):
        super(SceneWindow, self).mouseReleaseEvent(event)
        item = self.scene.itemAt(event.pos(), QTransform())
        if item:
            propertyDict = item.getProperties()
            self.showPropertyWindowSignal.emit(propertyDict)

    def resizeEvent(self, event):
        super(SceneWindow, self).resizeEvent(event)
        self.scene.setSceneRect(0, 0, self.width(), self.height())

    def keyPressEvent(self, event):
        super(SceneWindow, self).keyPressEvent(event)
        if event.key() == Qt.Key_Control:
            self.isCtrlPressed = True

    def keyReleaseEvent(self, event):
        super(SceneWindow, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_Control:
            self.isCtrlPressed = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())