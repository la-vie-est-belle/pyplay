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
        contentBackup = self.browser.contentBackup
        if contentBackup:
            self.browser.setHtml(contentBackup)

        if s.strip():
            html = self.browser.toHtml()
            lines = html.split('\n')

            matchList = []
            for line in lines[4:]:
                result = re.sub('(<p.*">)|(</span></p>)|(</body></html>)', '', line)
                if re.search(f'{s}', result, re.IGNORECASE):
                    matchList.append(line)

            if len(matchList):
                self.browser.setHtml(''.join(matchList))
            else:
                self.browser.setHtml('')


class Browser(QTextBrowser):
    def __init__(self):
        super(Browser, self).__init__()
        self.contentBackup = ''

        self.addInfo('asdsdsad')
        self.addWarning('asdasdasd')
        self.addError('adsdsad')

        self.main()

    def main(self):
        self.initWindowAttrs()

    def initWindowAttrs(self):
        self.setPlaceholderText('日志输出窗口')

    def addInfo(self, info):
        self.append(f'<span style="color:black">INFO: {info}</span>')
        self.contentBackup = self.toHtml()
        self.moveCursor(QTextCursor.End)

    def addWarning(self, warning):
        self.append(f'<span style="color:rgb(219, 207, 76)">WARN: {warning}</span>')
        self.contentBackup = self.toHtml()
        self.moveCursor(QTextCursor.End)

    def addError(self, error):
        self.append(f'<span style="color:red">ERROR: {error}</span>')
        self.contentBackup = self.toHtml()
        self.moveCursor(QTextCursor.End)

    def clear(self):
        super(Browser, self).clear()
        self.contentBackup = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = ConsoleWindow()
    assetWindow.show()
    sys.exit(app.exec())
