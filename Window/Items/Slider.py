from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Slider(QGraphicsProxyWidget):
    deleteSignal = pyqtSignal(str)

    def __init__(self, UUID, parentItem):
        super(Slider, self).__init__(parentItem)
        self.UUID = UUID
        self.startPos = QPoint()

        self.slider = QSlider(Qt.Horizontal)
        self.contextMenu = ContextMenu(self)

        self.main()

    def main(self):
        self.initWidgets()
        self.initSignals()

    def initWidgets(self):
        self.setWidget(self.slider)
        self.slider.setAttribute(Qt.WA_TranslucentBackground)

        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor(0, 105, 255, 128))
        # self.setPalette(palette)

    def initSignals(self):
        ...

    """Slots"""
    def delete(self):
        choice = QMessageBox.question(self.scene().views()[0], '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return

        childItems = self.childItems()
        for child in childItems:
            child.scene().removeItem(child)

        self.deleteLater()
        self.deleteSignal.emit(self.UUID)

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())

    def grabMouseEvent(self, event):
        super(Slider, self).grabMouseEvent(event)
        self.setCursor(Qt.OpenHandCursor)

    def ungrabMouseEvent(self, event):
        super(Slider, self).grabMouseEvent(event)
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(Slider, self).mousePressEvent(event)
        self.startPos = event.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        if self.startPos:
            newPos = event.pos()
            self.moveBy(newPos.x() - self.startPos.x(), newPos.y() - self.startPos.y())

    def mouseReleaseEvent(self, event):
        super(Slider, self).mouseMoveEvent(event)
        self.startPos = QPoint()


class ContextMenu(QObject):
    deleteSignal = pyqtSignal()

    def __init__(self, widget):
        super(ContextMenu, self).__init__()
        self.widget = widget
        self.mainMenu = QMenu()

        self.deleteAction = QAction('删除', self.mainMenu)

        self.main()

    def main(self):
        self.initSignals()
        self.setMainMenu()

    def initSignals(self):
        self.deleteAction.triggered.connect(self.widget.delete)

    def setMainMenu(self):
        self.mainMenu.addAction(self.deleteAction)

    def execMainMenu(self, pos):
        self.mainMenu.exec(pos)