from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from util import setItemAlignment


class Label(QGraphicsProxyWidget):
    deleteSignal = pyqtSignal(str)

    def __init__(self, UUID, parentItem):
        super(Label, self).__init__(parentItem)
        self.UUID = UUID
        self.startPos = QPoint()

        self.label = QLabel()
        self.contextMenu = ContextMenu(self)

        self.main()

    def __str__(self):
        return 'Label'

    def main(self):
        self.initWidgets()
        self.initSignals()

    def initWidgets(self):
        self.setWidget(self.label)
        self.label.setText('Label')
        self.label.setAttribute(Qt.WA_TranslucentBackground)

        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor(0, 105, 255, 128))
        # self.setPalette(palette)

    def initSignals(self):
        ...

    def getProperties(self):
        propertyDict = {'type': 'Label',
                        'UUID': self.UUID,
                        'posX': str(self.label.pos().x()),
                        'posY': str(self.label.pos().y()),
                        'text': self.label.text(),
                        'alignment': int(self.label.alignment()),
                        'font': f'{self.label.font().family()} ; {self.label.font().pointSize()}',
                        'color': self.label.palette().color(QPalette.WindowText).name()}
        return propertyDict

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

    def updateProperties(self, propertyDict):
        self.label.move(int(propertyDict['posX']), int(propertyDict['posY']))
        self.label.setText(propertyDict['text'])
        setItemAlignment(self.label, propertyDict['alignment'])

        newfontFamily = propertyDict['font'].split(' ; ')[0]
        newfontSize = int(propertyDict['font'].split(' ; ')[1])
        font = QFont(newfontFamily, newfontSize)
        self.label.setFont(font)
        self.label.adjustSize()

        palette = self.label.palette()
        palette.setColor(QPalette.WindowText, QColor(str(propertyDict['color'])))
        self.label.setPalette(palette)

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.execMainMenu(event.screenPos())

    def grabMouseEvent(self, event):
        super(Label, self).grabMouseEvent(event)
        self.setCursor(Qt.OpenHandCursor)

    def ungrabMouseEvent(self, event):
        super(Label, self).grabMouseEvent(event)
        self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(Label, self).mousePressEvent(event)
        self.startPos = event.pos()
        event.accept()

    def mouseMoveEvent(self, event):
        super(Label, self).mouseMoveEvent(event)
        if self.startPos:
            newPos = event.pos()
            self.moveBy(newPos.x() - self.startPos.x(), newPos.y() - self.startPos.y())

    def mouseReleaseEvent(self, event):
        super(Label, self).mouseMoveEvent(event)
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