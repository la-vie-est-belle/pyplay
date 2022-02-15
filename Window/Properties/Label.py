import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from util import getImagePath


class LabelPropertyWindow(QWidget):
    def __init__(self):
        super(LabelPropertyWindow, self).__init__()
        # 位置、大小、内容、对齐方式、字体、颜色

        self.xPosLineEdit = QLineEdit()
        self.yPosLineEdit = QLineEdit()
        self.xScaleLineEdit = QLineEdit()
        self.yScaleLineEdit = QLineEdit()
        self.textEdit = QTextEdit()

        self.alignLeftBtn = QPushButton()
        self.alignHCenterBtn = QPushButton()
        self.alignRightBtn = QPushButton()
        self.alignTopBtn = QPushButton()
        self.alignVCenterBtn = QPushButton()
        self.alignBottomBtn = QPushButton()

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
        self.xScaleLineEdit.setText('1')
        self.yScaleLineEdit.setText('1')

        self.textEdit.setPlaceholderText('请输入文本内容')

        self.alignLeftBtn.setIcon(QIcon(getImagePath('alignLeft.png')))
        self.alignHCenterBtn.setIcon(QIcon(getImagePath('alignHCenter.png')))
        self.alignRightBtn.setIcon(QIcon(getImagePath('alignRight.png')))
        self.alignTopBtn.setIcon(QIcon(getImagePath('alignTop.png')))
        self.alignVCenterBtn.setIcon(QIcon(getImagePath('alignVCenter.png')))
        self.alignBottomBtn.setIcon(QIcon(getImagePath('alignBottom.png')))

    def initSignals(self):
        ...

    def initLayouts(self):
        layout1 = QHBoxLayout()
        layout1.addWidget(QLabel('位置：'))
        layout1.addWidget(QLabel('x:'))
        layout1.addWidget(self.xPosLineEdit)
        layout1.addStretch()
        layout1.addWidget(QLabel('y:'))
        layout1.addWidget(self.yPosLineEdit)

        layout2 = QHBoxLayout()
        layout2.addWidget(QLabel('缩放：'))
        layout2.addWidget(QLabel('x:'))
        layout2.addWidget(self.xScaleLineEdit)
        layout2.addStretch()
        layout2.addWidget(QLabel('y:'))
        layout2.addWidget(self.yScaleLineEdit)

        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel('文本：'))
        layout3.addWidget(self.textEdit)

        layout4 = QHBoxLayout()
        layout4.addWidget(QLabel('水平对齐：'))
        layout4.addWidget(self.alignLeftBtn)
        layout4.addWidget(self.alignHCenterBtn)
        layout4.addWidget(self.alignRightBtn)

        layout5 = QHBoxLayout()
        layout5.addWidget(QLabel('垂直对齐：'))
        layout5.addWidget(self.alignTopBtn)
        layout5.addWidget(self.alignVCenterBtn)
        layout5.addWidget(self.alignBottomBtn)

        layout6 = QHBoxLayout()
        layout6.addWidget(QLabel('字体：'))
        layout6.addWidget(self.fontEdit)

        layout7 = QHBoxLayout()
        layout7.addWidget(QLabel('颜色：'))
        layout7.addWidget(self.colorEdit)

        windowLayout = QVBoxLayout(self)
        windowLayout.addLayout(layout1)
        windowLayout.addLayout(layout2)
        windowLayout.addLayout(layout3)
        windowLayout.addLayout(layout4)
        windowLayout.addLayout(layout5)
        windowLayout.addLayout(layout6)
        windowLayout.addLayout(layout7)


class FontEdit(QLineEdit):
    def __init__(self):
        super(FontEdit, self).__init__()
        self.setPlaceholderText('点击设置字体')
        self.setReadOnly(True)

    def mousePressEvent(self, event):
        super(FontEdit, self).mousePressEvent(event)
        font, ok = QFontDialog.getFont()
        if ok:
            self.setText(f'{font.family()} {font.pointSize()}')


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

            palette = self.palette()
            palette.setColor(QPalette.Base, color)
            self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = LabelPropertyWindow()
    a.show()
    sys.exit(app.exec())

