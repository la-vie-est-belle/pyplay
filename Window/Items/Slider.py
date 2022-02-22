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

        self.main()

    def __str__(self):
        return 'Slider'

    def main(self):
        self.initWidgets()
        self.initSignals()

    def initWidgets(self):
        self.setWidget(self.slider)
        self.slider.setAttribute(Qt.WA_TranslucentBackground)

        # 选中时的效果
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255, 80))
        self.setPalette(palette)

    def initSignals(self):
        ...

    def getProperties(self):
        propertyDict = {
                        'type': 'Slider',
                        'UUID': self.UUID,
                        'posX': str(self.slider.pos().x()),
                        'posY': str(self.slider.pos().y()),
                        'width': str(self.slider.width()),
                        'height': str(self.slider.height()),
                        'value': str(self.slider.value()),
                        'step': str(self.slider.singleStep()),
                        'min': str(self.slider.minimum()),
                        'max': str(self.slider.maximum()),
                        'orientation': self.slider.orientation(),
                       }
        return propertyDict

    def setProperties(self, propertyDict):
        self.slider.move(int(propertyDict['posX']), int(propertyDict['posY']))
        self.slider.resize(int(propertyDict['width']), int(propertyDict['height']))
        self.slider.setValue(int(propertyDict['value']))
        self.slider.setMinimum(int(propertyDict['min']))
        self.slider.setMaximum(int(propertyDict['max']))
        self.slider.setSingleStep(int(propertyDict['step']))
        self.slider.setOrientation(propertyDict['orientation'])

    def setSelected(self, isSelected):
        if isSelected:
            self.setAutoFillBackground(True)
        else:
            self.setAutoFillBackground(False)

    def delete(self):
        choice = QMessageBox.question(self.scene().views()[0], '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return

        self.scene().removeItem(self)
        self.deleteSignal.emit(self.UUID)

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
