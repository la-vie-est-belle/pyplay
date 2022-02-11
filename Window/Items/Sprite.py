import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Sprite(QGraphicsPixmapItem):
    def __init__(self):
        super(Sprite, self).__init__()
        self.contextMenu = ContextMenuForSprite()
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
        self.scene().removeItem(self)

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())


class ContextMenuForSprite(QObject):
    editSignal = pyqtSignal()
    deleteSignal = pyqtSignal()

    def __init__(self):
        super(ContextMenuForSprite, self).__init__()
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

