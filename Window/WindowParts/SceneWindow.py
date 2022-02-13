import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Window.Items.Label import Label
from Window.Items.Sprite import Sprite
from Window.Items.Button import Button


class SceneWindow(QGraphicsView):
    deleteSignal = pyqtSignal(str)
    clickSignal = pyqtSignal(list)

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
                    print(UUID)
                    self.scene.removeItem(item)
                    break

    def add(self, itemName, UUID, parentUUID):
        # 先找到父项
        parentItem = None
        if parentUUID:
            items = self.scene.items()
            for item in items:
                if item.UUID == parentUUID:
                    parentItem = item
                    break

        # 再生成相应的项
        if itemName == 'Button':
            self.addButton(UUID, parentItem)
        if itemName == 'Label':
            self.addLabel(UUID, parentItem)
        elif itemName == 'Sprite':
            self.addSprite(UUID, parentItem)

    def addButton(self, UUID, parentItem):
        button = Button(UUID, parentItem)

        if not parentItem:
            self.scene.addItem(button)

    def addLabel(self, UUID, parentItem):
        label = Label(UUID, parentItem)
        label.setHtml('Hello PyPlay')

        label.deleteSignal.connect(lambda: self.deleteSignal.emit(label.UUID))
        if not parentItem:
            self.scene.addItem(label)

    def addLineEdit(self, UUID):
        ...

    def addSlider(self, UUID):
        ...

    def addSprite(self, UUID, parentItem):
        sprite = Sprite(UUID, parentItem)
        sprite.setPixmap(QPixmap('/Users/louis/Desktop/pyplay/res/d7e409bfa2ee4e3b956738ca1f6445e8.png'))

        # QGraphiscPixmapItem无法转换成QObject，所以无法发送信号。
        # 可以通过它的contextMenu直接发送 (这是特使情况，如果有其他Item出现类似的情形，就用这种办法解决)
        sprite.contextMenu.deleteSignal.connect(lambda: self.deleteSignal.emit(sprite.UUID))
        if not parentItem:
            self.scene.addItem(sprite)

    """Events"""
    # mousePressEvent有个多选bug，所以改为用mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        super(SceneWindow, self).mouseReleaseEvent(event)
        UUIDList = []
        for item in self.scene.selectedItems():
            UUIDList.append(item.UUID)

        if UUIDList:
            self.clickSignal.emit(UUIDList)

    def paintEvent(self, event):
        super(SceneWindow, self).paintEvent(event)

        # 这段代码应该要放在mousePressEvent中的
        # 但是鼠标点击事件不能实时获取多选的item
        # UUIDList = []
        # for item in self.scene.selectedItems():
        #     UUIDList.append(item.UUID)
        #
        # if UUIDList:
        #     self.clickSignal.emit(UUIDList)

    def resizeEvent(self, event):
        super(SceneWindow, self).resizeEvent(event)
        self.scene.setSceneRect(0, 0, self.width(), self.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = SceneWindow()
    assetWindow.show()
    sys.exit(app.exec())