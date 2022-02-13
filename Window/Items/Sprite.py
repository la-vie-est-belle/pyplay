from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Sprite(QGraphicsPixmapItem):
    # deleteSignal = pyqtSignal(str)

    def __init__(self, UUID, parentItem):
        super(Sprite, self).__init__(parentItem)
        self.UUID = UUID
        self.contextMenu = ContextMenuForSprite(self)
        self.main()

    def main(self):
        self.initItemAttrs()
        self.initSignals()

    def initItemAttrs(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def initSignals(self):
        self.contextMenu.editSignal.connect(self.edit)
        self.contextMenu.deleteSignal.connect(self.delete)

    """Slots"""
    def edit(self):
        ...

    def delete(self):
        choice = QMessageBox.question(self.scene().views()[0], '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            childItems = self.childItems()
            for child in childItems:
                child.scene().removeItem(child)

            self.scene().removeItem(self)
            # self.deleteSignal.emit(self.UUID)

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())


class ContextMenuForSprite(QObject):
    editSignal = pyqtSignal()
    deleteSignal = pyqtSignal()

    def __init__(self, sprite):
        super(ContextMenuForSprite, self).__init__()
        self.sprite = sprite
        self.mainMenu = QMenu()

        self.editAction = QAction('编辑', self.mainMenu)
        self.deleteAction = QAction('删除', self.mainMenu)

        self.main()

    def main(self):
        self.initSignals()
        self.setMainMenu()

    def initSignals(self):
        self.editAction.triggered.connect(self.editSignal.emit)
        self.deleteAction.triggered.connect(self.deleteSignal.emit)

    def setMainMenu(self):
        self.mainMenu.addAction(self.editAction)
        self.mainMenu.addAction(self.deleteAction)

    def execMainMenu(self, pos):
        self.mainMenu.exec(pos)

