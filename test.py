import sys
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QPainterPath
from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsEllipseItem, \
    QGraphicsPixmapItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsScene, QGraphicsView


from Window.Items.Label import Label


class Demo(QGraphicsView):
    def __init__(self):
        super(Demo, self).__init__()
        # 1
        self.resize(300, 300)

        # 2
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 300, 300)

        # 6
        self.pic = QGraphicsPixmapItem()
        self.pic.setPixmap(QPixmap('pic.png').scaled(60, 60))
        self.pic.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.pic.setOffset(100, 120)
        # self.pic.setOffset(QPointF(100, 120))

        self.text2 = Label()
        self.text2.setHtml('Hello World')
        # self.text2.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.text2.setPos(100, 200)

        # 9
        self.scene.addItem(self.pic)
        self.scene.addItem(self.text2)

        # 10
        self.setScene(self.scene)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())