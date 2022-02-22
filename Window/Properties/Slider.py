import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from util import getImagePath


class SliderPropertyWindow(QWidget):
    updateItemSignal = pyqtSignal(dict)

    def __init__(self):
        super(SliderPropertyWindow, self).__init__()
        # 位置、大小、方向、当前数值、最大值、最小值、步长
        self.UUID = ''
        self.propertyDict = {}

        self.posXLineEdit = QLineEdit()
        self.posYLineEdit = QLineEdit()
        self.widthLineEdit = QLineEdit()
        self.heightLineEdit = QLineEdit()

        self.hOrientationBtn = QPushButton()
        self.vOrientationBtn = QPushButton()

        self.valueLineEdit = QLineEdit()
        self.minLineEdit = QLineEdit()
        self.maxLineEdit = QLineEdit()
        self.stepLineEdit = QLineEdit()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        ...

    def initWidgets(self):
        self.posXLineEdit.setText('0')
        self.posYLineEdit.setText('0')
        self.posXLineEdit.setValidator(QRegExpValidator(QRegExp('-?[0-9]+')))
        self.posYLineEdit.setValidator(QRegExpValidator(QRegExp('-?[0-9]+')))

        self.widthLineEdit.setText('200')
        self.heightLineEdit.setText('22')
        self.widthLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.heightLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))

        self.hOrientationBtn.setIcon(QIcon(getImagePath('horizontalSlider.png')))
        self.vOrientationBtn.setIcon(QIcon(getImagePath('verticalSlider.png')))
        self.hOrientationBtn.setEnabled(False)

        self.valueLineEdit.setText('0')
        self.minLineEdit.setText('0')
        self.maxLineEdit.setText('99')
        self.stepLineEdit.setText('1')
        self.valueLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.minLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.maxLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.stepLineEdit.setValidator(QRegExpValidator(QRegExp('[0-9]+')))

    def initSignals(self):
        self.posXLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('posX', self.posXLineEdit.text().strip()))
        self.posYLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('posY', self.posYLineEdit.text().strip()))

        self.widthLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('width', self.widthLineEdit.text().strip()))
        self.heightLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('height', self.heightLineEdit.text().strip()))
        self.valueLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('value', self.valueLineEdit.text().strip()))
        self.minLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('min', self.minLineEdit.text().strip()))
        self.maxLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('max', self.maxLineEdit.text().strip()))
        self.stepLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('step', self.stepLineEdit.text().strip()))

        self.hOrientationBtn.clicked.connect(lambda: self.updateItemPropertiesOnScene('orientation', 1))
        self.vOrientationBtn.clicked.connect(lambda: self.updateItemPropertiesOnScene('orientation', 2))


    def initLayouts(self):
        posHlayout = QHBoxLayout()
        posHlayout.addWidget(QLabel('位置：'))
        posHlayout.addWidget(QLabel('x:'))
        posHlayout.addWidget(self.posXLineEdit)
        posHlayout.addStretch()
        posHlayout.addWidget(QLabel('y:'))
        posHlayout.addWidget(self.posYLineEdit)

        sizeHlayout = QHBoxLayout()
        sizeHlayout.addWidget(QLabel('尺寸：'))
        sizeHlayout.addWidget(QLabel('宽度：'))
        sizeHlayout.addWidget(self.widthLineEdit)
        sizeHlayout.addStretch()
        sizeHlayout.addWidget(QLabel('高度：'))
        sizeHlayout.addWidget(self.heightLineEdit)

        valueHLayout = QHBoxLayout()
        valueHLayout.addWidget(QLabel('值：'))
        valueHLayout.addWidget(self.valueLineEdit)

        stepHLayout = QHBoxLayout()
        stepHLayout.addWidget(QLabel('步长：'))
        stepHLayout.addWidget(self.stepLineEdit)

        minMaxHlayout = QHBoxLayout()
        minMaxHlayout.addWidget(QLabel('最小值：'))
        minMaxHlayout.addWidget(self.minLineEdit)
        minMaxHlayout.addStretch()
        minMaxHlayout.addWidget(QLabel('最大值：'))
        minMaxHlayout.addWidget(self.maxLineEdit)

        orientationBtnHLayout = QHBoxLayout()
        orientationBtnHLayout.addWidget(QLabel('方向：'))
        orientationBtnHLayout.addWidget(self.hOrientationBtn)
        orientationBtnHLayout.addWidget(self.vOrientationBtn)
        orientationBtnHLayout.addStretch()

        windowLayout = QVBoxLayout(self)
        windowLayout.addLayout(posHlayout)
        windowLayout.addLayout(sizeHlayout)
        windowLayout.addLayout(valueHLayout)
        windowLayout.addLayout(stepHLayout)
        windowLayout.addLayout(minMaxHlayout)
        windowLayout.addLayout(orientationBtnHLayout)
        windowLayout.addStretch()

    def setPropertyWindowValues(self, propertyDict):
        self.propertyDict = propertyDict
        self.UUID = propertyDict['UUID']

        if self.posXLineEdit.text() != propertyDict['posX']:
            self.posXLineEdit.setText(propertyDict['posX'])

        if self.posYLineEdit.text() != propertyDict['posY']:
            self.posYLineEdit.setText(propertyDict['posY'])

        if self.widthLineEdit.text() != propertyDict['width']:
            self.posYLineEdit.setText(propertyDict['width'])

        if self.heightLineEdit.text() != propertyDict['height']:
            self.heightLineEdit.setText(propertyDict['height'])

        if self.valueLineEdit.text() != propertyDict['value']:
            self.valueLineEdit.setText(propertyDict['value'])

        if self.stepLineEdit.text() != propertyDict['step']:
            self.stepLineEdit.setText(propertyDict['step'])

        if self.minLineEdit.text() != propertyDict['min']:
            self.minLineEdit.setText(propertyDict['min'])

        if self.maxLineEdit.text() != propertyDict['max']:
            self.maxLineEdit.setText(propertyDict['max'])

        if self.propertyDict['orientation'] == 1:
            self.hOrientationBtn.setEnabled(False)
            self.vOrientationBtn.setEnabled(True)
        else:
            self.hOrientationBtn.setEnabled(True)
            self.vOrientationBtn.setEnabled(False)

    def updateItemPropertiesOnScene(self, property, value):
        if property == 'posX' and not value:
            self.posXLineEdit.setText('0')
            return
        elif property == 'posY' and not value:
            self.posYLineEdit.setText('0')
            return
        elif property == 'width' and not value:
            self.widthLineEdit.setText('0')
            return
        elif property == 'height' and not value:
            self.heightLineEdit.setText('0')
            return
        elif property == 'value' and not value:
            self.valueLineEdit.setText('0')
            return
        elif property == 'min' and not value:
            self.minLineEdit.setText('0')
            return
        elif property == 'max' and not value:
            self.maxLineEdit.setText('0')
            return
        elif property == 'step' and not value:
            self.stepLineEdit.setText('1')
            return

        elif property == 'value':
            if int(value) > int(self.maxLineEdit.text().strip()):
                QMessageBox.critical(self, '错误', '不允许大于最大值！')
                self.valueLineEdit.setText(self.maxLineEdit.text())
                return
            elif int(value) < int(self.minLineEdit.text().strip()):
                QMessageBox.critical(self, '错误', '不允许小于最小值！')
                self.valueLineEdit.setText(self.minLineEdit.text())
                return

        elif property == 'min':
            if int(value) > int(self.maxLineEdit.text().strip()):
                QMessageBox.critical(self, '错误', '最小值不能大于最大值！')
                self.minLineEdit.setText(self.maxLineEdit.text())
                return

            if int(value) > int(self.valueLineEdit.text()):
                self.valueLineEdit.setText(value)

        elif property == 'max':
            if int(value) < int(self.minLineEdit.text().strip()):
                QMessageBox.critical(self, '错误', '最大值不能小于最小值！')
                self.maxLineEdit.setText(self.minLineEdit.text())
                return

            if int(value) < int(self.valueLineEdit.text()):
                self.valueLineEdit.setText(value)

        elif property == 'orientation':
            if value == 1:
                self.hOrientationBtn.setEnabled(False)
                self.vOrientationBtn.setEnabled(True)
            else:
                self.hOrientationBtn.setEnabled(True)
                self.vOrientationBtn.setEnabled(False)
            temp = self.heightLineEdit.text()
            self.heightLineEdit.setText(self.widthLineEdit.text())
            self.widthLineEdit.setText(temp)

        self.propertyDict[property] = value
        self.updateItemSignal.emit(self.propertyDict)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = SliderPropertyWindow()
    a.show()
    sys.exit(app.exec())

