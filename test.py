import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import *


class Demo(QGraphicsView):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(600, 600)
        self.setAlignment(Qt.AlignTop)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 300, 300)

        self.rect = self.scene.addRect(0, 0, 100, 30)
        self.rect2 = self.scene.addRect(300, 300, 100, 30)
        self.ellipse = self.scene.addEllipse(100, 80, 50, 40)
        self.pic = self.scene.addPixmap(QPixmap('pic.png').scaled(60, 60))
        self.pic.setOffset(100, 130)

        rect = QGraphicsRectItem(100, 30, 10, 10, self.rect)
        self.scene.addItem(rect)

        self.rect.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.ellipse.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.pic.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        self.setScene(self.scene)

    def mouseDoubleClickEvent(self, event):
        item = self.scene.itemAt(event.pos(), QTransform())
        self.scene.removeItem(item)
        super().mouseDoubleClickEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())