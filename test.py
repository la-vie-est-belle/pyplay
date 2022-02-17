import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import *


class Demo(QLabel):
    def __init__(self):
        super(Demo, self).__init__()
        # left 1
        # right 2
        # hcenter 4

        # top 32
        # bottom 64
        # vcenter 128

        # left | top   33
        # left | bottom 65
        # left | vcenter 129

        # right | top   34
        # right | bottom 66
        # right | vcenter 130

        # hcenter | top   36
        # hcenter | bottom 68
        # hcenter | vcenter 132
        self.setAlignment(Qt.AlignVCenter)
        print(int(self.alignment()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())