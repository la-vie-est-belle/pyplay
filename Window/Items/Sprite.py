import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Sprite(QGraphicsPixmapItem):
    def __init__(self):
        super(Sprite, self).__init__()
        self.main()

    def main(self):
        self.initItemAttrs()

    def initItemAttrs(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

