import sys
from PyQt5.QtWidgets import *


class EditWindow(QMainWindow):
    def __init__(self):
        super(EditWindow, self).__init__()
        self.hierarchyWindow = None
        self.assetsWindow = None
        self.sceneWindow = None
        self.previewWindow = None
        self.propertyWindow = None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editWindow = EditWindow()
    editWindow.show()
    sys.exit(app.exec())
