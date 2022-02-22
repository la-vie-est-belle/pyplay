import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from util import getImagePath


class LabelPropertyWindow(QWidget):
    updateItemSignal = pyqtSignal(dict)

    def __init__(self):
        super(LabelPropertyWindow, self).__init__()
        self.UUID = ''
        self.propertyDict = {}

        self.posXLineEdit = QLineEdit()
        self.posYLineEdit = QLineEdit()
        self.textEdit = QTextEdit()

        self.alignLeftBtn = QPushButton()
        self.alignHCenterBtn = QPushButton()
        self.alignRightBtn = QPushButton()
        self.alignTopBtn = QPushButton()
        self.alignVCenterBtn = QPushButton()
        self.alignBottomBtn = QPushButton()
        self.hAlignBtnList = [self.alignLeftBtn, self.alignHCenterBtn, self.alignRightBtn]
        self.vAlignBtnList = [self.alignTopBtn, self.alignVCenterBtn, self.alignBottomBtn]

        self.fontEdit = FontEdit()
        self.colorEdit = ColorEdit()

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

        self.textEdit.setText('Label')
        self.textEdit.setPlaceholderText('请输入文本内容')

        self.alignLeftBtn.setIcon(QIcon(getImagePath('alignLeft.png')))
        self.alignHCenterBtn.setIcon(QIcon(getImagePath('alignHCenter.png')))
        self.alignRightBtn.setIcon(QIcon(getImagePath('alignRight.png')))
        self.alignTopBtn.setIcon(QIcon(getImagePath('alignTop.png')))
        self.alignVCenterBtn.setIcon(QIcon(getImagePath('alignVCenter.png')))
        self.alignBottomBtn.setIcon(QIcon(getImagePath('alignBottom.png')))

        self.alignLeftBtn.setProperty('alignment', Qt.AlignLeft)
        self.alignHCenterBtn.setProperty('alignment', Qt.AlignHCenter)
        self.alignRightBtn.setProperty('alignment', Qt.AlignRight)
        self.alignTopBtn.setProperty('alignment', Qt.AlignTop)
        self.alignVCenterBtn.setProperty('alignment', Qt.AlignVCenter)
        self.alignBottomBtn.setProperty('alignment', Qt.AlignBottom)

        self.alignLeftBtn.setEnabled(False)
        self.alignVCenterBtn.setEnabled(False)

    def initSignals(self):
        self.alignLeftBtn.clicked.connect(self.setHorizontalAlignmentBtnEnabled)
        self.alignHCenterBtn.clicked.connect(self.setHorizontalAlignmentBtnEnabled)
        self.alignRightBtn.clicked.connect(self.setHorizontalAlignmentBtnEnabled)
        self.alignTopBtn.clicked.connect(self.setVerticalAlignmentBtnEnabled)
        self.alignVCenterBtn.clicked.connect(self.setVerticalAlignmentBtnEnabled)
        self.alignBottomBtn.clicked.connect(self.setVerticalAlignmentBtnEnabled)

        self.posXLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('posX', self.posXLineEdit.text().strip()))
        self.posYLineEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('posY', self.posYLineEdit.text().strip()))
        self.textEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('text', self.textEdit.toPlainText().strip()))
        self.fontEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('font', self.fontEdit.text().strip()))
        self.colorEdit.textChanged.connect(lambda: self.updateItemPropertiesOnScene('color', self.colorEdit.text().strip()))

    def initLayouts(self):
        posHlayout = QHBoxLayout()
        posHlayout.addWidget(QLabel('位置：'))
        posHlayout.addWidget(QLabel('x:'))
        posHlayout.addWidget(self.posXLineEdit)
        posHlayout.addStretch()
        posHlayout.addWidget(QLabel('y:'))
        posHlayout.addWidget(self.posYLineEdit)

        textVlayout = QVBoxLayout()
        textVlayout.addWidget(QLabel('文本：'))
        textVlayout.addWidget(self.textEdit)

        alignBtnHLayout = QHBoxLayout()
        alignBtnHLayout.addWidget(QLabel('水平对齐：'))
        alignBtnHLayout.addWidget(self.alignLeftBtn)
        alignBtnHLayout.addWidget(self.alignHCenterBtn)
        alignBtnHLayout.addWidget(self.alignRightBtn)

        alignBtnHLayout2 = QHBoxLayout()
        alignBtnHLayout2.addWidget(QLabel('垂直对齐：'))
        alignBtnHLayout2.addWidget(self.alignTopBtn)
        alignBtnHLayout2.addWidget(self.alignVCenterBtn)
        alignBtnHLayout2.addWidget(self.alignBottomBtn)

        fontHLayout = QHBoxLayout()
        fontHLayout.addWidget(QLabel('字体：'))
        fontHLayout.addWidget(self.fontEdit)

        colorHLayout = QHBoxLayout()
        colorHLayout.addWidget(QLabel('颜色：'))
        colorHLayout.addWidget(self.colorEdit)

        windowLayout = QVBoxLayout(self)
        windowLayout.addLayout(posHlayout)
        windowLayout.addLayout(textVlayout)
        windowLayout.addLayout(alignBtnHLayout)
        windowLayout.addLayout(alignBtnHLayout2)
        windowLayout.addLayout(fontHLayout)
        windowLayout.addLayout(colorHLayout)
        windowLayout.addStretch()

    def setHorizontalAlignmentBtnEnabled(self):
        hBtn = None
        for btn in self.hAlignBtnList:
            if btn == self.sender():
                btn.setEnabled(False)
                hBtn = btn
            else:
                btn.setEnabled(True)

        vBtn = None
        for btn in self.vAlignBtnList:
            if not btn.isEnabled():
                vBtn = btn
                break

        self.updateItemPropertiesOnScene('alignment', hBtn.property('alignment')|vBtn.property('alignment'))

    def setVerticalAlignmentBtnEnabled(self):
        vBtn = None
        for btn in self.vAlignBtnList:
            if btn == self.sender():
                btn.setEnabled(False)
                vBtn = btn
            else:
                btn.setEnabled(True)

        hBtn = None
        for btn in self.hAlignBtnList:
            if not btn.isEnabled():
                hBtn = btn
                break

        self.updateItemPropertiesOnScene('alignment', hBtn.property('alignment') | vBtn.property('alignment'))

    def setAlignBtnEnabled(self, alignment):
        for btn in self.hAlignBtnList:
            btn.setEnabled(True)
        for btn in self.vAlignBtnList:
            btn.setEnabled(True)

        # if alignment == 1:
        #     self.alignLeftBtn.setEnabled(False)
        # elif alignment == 2:
        #     self.alignRightBtn.setEnabled(False)
        # elif alignment == 4:
        #     self.alignHCenterBtn.setEnabled(False)
        # elif alignment == 32:
        #     self.alignTopBtn.setEnabled(False)
        # elif alignment == 64:
        #     self.alignBottomBtn.setEnabled(False)
        # elif alignment == 128:
        #     self.alignVCenterBtn.setEnabled(False)

        # 从场景中发过来对齐方式肯定是水平和垂直两个方向上一起的
        if alignment == 33:
            self.alignLeftBtn.setEnabled(False)
            self.alignTopBtn.setEnabled(False)
        elif alignment == 65:
            self.alignLeftBtn.setEnabled(False)
            self.alignBottomBtn.setEnabled(False)
        elif alignment == 129:
            self.alignLeftBtn.setEnabled(False)
            self.alignVCenterBtn.setEnabled(False)
        elif alignment == 34:
            self.alignRightBtn.setEnabled(False)
            self.alignTopBtn.setEnabled(False)
        elif alignment == 66:
            self.alignRightBtn.setEnabled(False)
            self.alignBottomBtn.setEnabled(False)
        elif alignment == 130:
            self.alignRightBtn.setEnabled(False)
            self.alignVCenterBtn.setEnabled(False)
        elif alignment == 36:
            self.alignHCenterBtn.setEnabled(False)
            self.alignTopBtn.setEnabled(False)
        elif alignment == 68:
            self.alignHCenterBtn.setEnabled(False)
            self.alignBottomBtn.setEnabled(False)
        elif alignment == 132:
            self.alignHCenterBtn.setEnabled(False)
            self.alignVCenterBtn.setEnabled(False)

    def setPropertyWindowValues(self, propertyDict):
        self.propertyDict = propertyDict
        self.UUID = propertyDict['UUID']

        if self.posXLineEdit.text() != propertyDict['posX']:
            self.posXLineEdit.setText(propertyDict['posX'])

        if self.posYLineEdit.text() != propertyDict['posY']:
            self.posYLineEdit.setText(propertyDict['posY'])

        if self.textEdit.toPlainText() != propertyDict['text']:
            self.textEdit.setText(propertyDict['text'])

        self.setAlignBtnEnabled(propertyDict['alignment'])

        if self.fontEdit.text() != propertyDict['font']:
            self.fontEdit.setText(propertyDict['font'])

        if self.colorEdit.toolTip() != propertyDict['color']:
            palette = self.colorEdit.palette()
            palette.setColor(QPalette.Base, QColor(propertyDict['color']))
            self.colorEdit.setPalette(palette)
            self.colorEdit.setToolTip(propertyDict['color'])

    def updateItemPropertiesOnScene(self, property, value):
        if property == 'posX' and not value:
            self.posXLineEdit.setText('0')
            return
        elif property == 'posY' and not value:
            self.posYLineEdit.setText('0')
            return

        self.propertyDict[property] = value
        self.updateItemSignal.emit(self.propertyDict)


class FontEdit(QLineEdit):
    def __init__(self):
        super(FontEdit, self).__init__()
        self.setPlaceholderText('点击设置字体')
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        super(FontEdit, self).mousePressEvent(event)
        font, ok = QFontDialog.getFont()
        if ok:
            self.setText(f'{font.family()} ; {font.pointSize()}')


class ColorEdit(QLineEdit):
    def __init__(self):
        super(ColorEdit, self).__init__()
        self.setPlaceholderText('点击设置颜色')
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        super(ColorEdit, self).mousePressEvent(event)
        color = QColorDialog.getColor()
        if color.isValid():
            self.setPlaceholderText('')
            self.setToolTip(color.name())
            self.setText(color.name())

            palette = self.palette()
            palette.setColor(QPalette.Base, color)
            self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = LabelPropertyWindow()
    a.show()
    sys.exit(app.exec())

