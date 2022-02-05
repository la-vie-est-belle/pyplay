import re
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ConsoleWindow(QWidget):
    def __init__(self):
        super(ConsoleWindow, self).__init__()
        self.addBtn = QPushButton()
        self.clearBtn = QPushButton()
        self.searchLine = QLineEdit()
        self.browser = Browser()

        self.main()

    def main(self):
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWidgets(self):
        self.clearBtn.setText('Clear')
        self.searchLine.setPlaceholderText('搜索关键词')

    def initSignals(self):
        self.addBtn.clicked.connect(lambda: self.browser.addInfo('11111111'))
        self.clearBtn.clicked.connect(lambda: self.browser.clear())
        self.searchLine.textChanged.connect(self.search)

    def initLayouts(self):
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout(self)
        hLayout.setContentsMargins(0, 10, 0, 0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.setSpacing(10)
        vLayout.setSpacing(0)
        hLayout.addWidget(self.addBtn)
        hLayout.addWidget(self.clearBtn)
        hLayout.addWidget(self.searchLine)
        hLayout.addStretch()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.browser)

    """Slots"""
    def search(self, s):
        if s:
            # 将原本的html保存起来，替换为[[]]，高亮显示后，将html代码复原
            # print(self.browser.toPlainText())
            # print(self.browser.toHtml())
            # print(len(re.findall(f'{s}', self.browser.toPlainText(), re.IGNORECASE)))
            # values = self.browser.toPlainText().split(s)
            # newContent = f'<span style="background:yellow">{s}</span>'.join(values)
            # self.browser.setHtml(newContent)


class Browser(QTextBrowser):
    def __init__(self):
        super(Browser, self).__init__()
        self.main()
        for i in range(20):
            self.addInfo('asdsdsad')
        self.addWarning('asdasdasd')
        self.addError('adsdsad')

    def main(self):
        self.initWindowAttrs()

    def initWindowAttrs(self):
        ...

    def addInfo(self, info):
        self.append(f'<p style="color:black"><span style="font-weight:bold">INFO:</span> {info}</p>')
        self.moveCursor(QTextCursor.End)

    def addWarning(self, warning):
        self.append(f'<p style="color:rgb(219, 207, 76)"><span style="font-weight:bold">WARNING:</span> {warning}</p>')
        self.moveCursor(QTextCursor.End)

    def addError(self, error):
        self.append(f'<p style="color:red"><span style="font-weight:bold">ERROR:</span> {error}</p>')
        self.moveCursor(QTextCursor.End)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = ConsoleWindow()
    assetWindow.show()
    sys.exit(app.exec())
