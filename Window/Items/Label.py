import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Label(QGraphicsTextItem):
    def __init__(self):
        super(Label, self).__init__()
        self.contextMenu = ContextMenuForLabel()
        self.main()

    def main(self):
        self.initItemAttrs()
        self.initSignals()

    def initItemAttrs(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def initSignals(self):
        self.contextMenu.editSignal.connect(self.edit)
        self.contextMenu.deleteSignal.connect(self.delete)

    def moveCursorToEnd(self):
        cursor = self.textCursor()
        cursor.setPosition(len(self.toPlainText()))
        self.setTextCursor(cursor)

    """Slots"""
    def edit(self):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.moveCursorToEnd()

    def delete(self):
        self.deleteLater()

    """Events"""
    def mouseDoubleClickEvent(self, event):
        super(Label, self).mouseDoubleClickEvent(event)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.moveCursorToEnd()

    def keyPressEvent(self, event):
        super(Label, self).keyPressEvent(event)
        print(self.toPlainText())

    def focusOutEvent(self, event):
        super(Label, self).focusOutEvent(event)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.moveCursorToEnd()

    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())


class ContextMenuForLabel(QObject):
    editSignal = pyqtSignal()
    deleteSignal = pyqtSignal()

    def __init__(self):
        super(ContextMenuForLabel, self).__init__()
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
