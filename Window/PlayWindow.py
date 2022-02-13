import sys
from util import readQss
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from WindowParts.ItemWindow import ItemWindow
from WindowParts.AssetWindow import AssetWindow
from WindowParts.ConsoleWindow import ConsoleWindow
from WindowParts.SceneWindow import SceneWindow
from WindowParts.SceneWindowBase import SceneWindowBase


class PlayWindow(QMainWindow):
    def __init__(self):
        super(PlayWindow, self).__init__()
        self.allSplitter = QSplitter()
        self.leftSplitter = QSplitter()
        self.centerSplitter = QSplitter()

        self.leftTopTab = QTabWidget()
        self.leftBottomTab = QTabWidget()
        self.centerTopTab = QTabWidget()
        self.centerBottomTab = QTabWidget()
        self.rightTab = QTabWidget()

        self.itemWindow = None
        self.assetWindow = None
        self.sceneWindow = None
        self.sceneWindowBase = None
        self.consoleWindow = None
        self.propertyWindow = None

        self.windowCenterWidget = QWidget()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.resize(1400, 700)
        self.setWindowTitle('PyPlay')
        self.setCentralWidget(self.windowCenterWidget)

    def initWidgets(self):
        self.itemWindow = ItemWindow()
        self.assetWindow = AssetWindow()
        self.sceneWindow = SceneWindow()
        self.sceneWindowBase = SceneWindowBase()
        self.consoleWindow = ConsoleWindow()
        self.propertyWindow = QWidget()

        self.leftTopTab.addTab(self.itemWindow, '层级窗口')
        self.leftBottomTab.addTab(self.assetWindow, '资源窗口')
        self.centerTopTab.addTab(self.sceneWindowBase, '场景窗口')
        self.centerBottomTab.addTab(self.consoleWindow, '日志窗口')
        self.rightTab.addTab(self.propertyWindow, '属性窗口')

        self.leftSplitter.addWidget(self.leftTopTab)
        self.leftSplitter.addWidget(self.leftBottomTab)
        self.leftSplitter.setOrientation(Qt.Vertical)

        self.centerSplitter.addWidget(self.centerTopTab)
        self.centerSplitter.addWidget(self.centerBottomTab)
        self.centerSplitter.setOrientation(Qt.Vertical)
        self.centerSplitter.setSizes([500, 200])

        self.allSplitter.addWidget(self.leftSplitter)
        self.allSplitter.addWidget(self.centerSplitter)
        self.allSplitter.addWidget(self.rightTab)
        self.allSplitter.setSizes([300, 800, 300])

    def initSignals(self):
        self.itemWindow.addSignal.connect(self.sceneWindow.add)
        self.itemWindow.deleteSignal.connect(self.sceneWindow.delete)
        self.itemWindow.clickSignal.connect(self.sceneWindow.focus)

        self.sceneWindow.deleteSignal.connect(self.itemWindow.delete)
        self.sceneWindow.clickSignal.connect(self.itemWindow.focus)

    def initLayouts(self):
        hLayout1 = QHBoxLayout(self.sceneWindowBase)
        hLayout1.addWidget(self.sceneWindow)

        hLayout2 = QHBoxLayout(self.windowCenterWidget)
        hLayout2.addWidget(self.allSplitter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    playWindow = PlayWindow()
    playWindow.setStyleSheet(readQss('../res/qss/default.qss'))
    playWindow.show()
    sys.exit(app.exec())
