import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Label(QGraphicsTextItem):
    def __init__(self):
        super(Label, self).__init__()
        self.main()

    def main(self):
        self.initItemAttrs()

    def initItemAttrs(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

    def moveCursorToEnd(self):
        cursor = self.textCursor()
        cursor.setPosition(len(self.toPlainText()))
        self.setTextCursor(cursor)

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
        ...