from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Button(QGraphicsProxyWidget):
    def __init__(self, UUID, parentItem):
        super(Button, self).__init__(parentItem)
        self.startPos = QPoint()
        self.UUID = UUID

        self.button = QPushButton()
        self.contextMenu = ContextMenu()

        self.main()

    def main(self):
        self.initItemAttrs()
        self.initSignals()

    def initItemAttrs(self):
        self.setWidget(self.button)
        self.button.setText('Button')
        self.button.setAttribute(Qt.WA_TranslucentBackground)
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def initSignals(self):
        self.contextMenu.editSignal.connect(self.edit)
        self.contextMenu.deleteSignal.connect(self.delete)

    """Slots"""
    def edit(self):
        ...

    def delete(self):
        self.deleteLater()

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())

    def mousePressEvent(self, event):
        super(Button, self).mousePressEvent(event)
        self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        super(Button, self).mouseMoveEvent(event)
        if self.startPos:
            currentPos = event.pos()
            self.moveBy(currentPos.x()-self.startPos.x(), currentPos.y()-self.startPos.y())

    def mouseReleaseEvent(self, event):
        super(Button, self).mouseMoveEvent(event)
        self.startPos = QPoint()
        

class ContextMenu(QObject):
    editSignal = pyqtSignal()
    deleteSignal = pyqtSignal()

    def __init__(self):
        super(ContextMenu, self).__init__()
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