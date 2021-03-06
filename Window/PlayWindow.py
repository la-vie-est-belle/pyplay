import sys
from util import readQss
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from WindowParts.ItemWindow import ItemWindow
from WindowParts.AssetWindow import AssetWindow
from WindowParts.ConsoleWindow import ConsoleWindow
from WindowParts.SceneWindow import SceneWindow
from WindowParts.SceneWindowBase import SceneWindowBase

from Properties.Label import LabelPropertyWindow
from Properties.Slider import SliderPropertyWindow


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

        self.itemWindow = ItemWindow()
        self.assetWindow = AssetWindow()
        self.sceneWindow = SceneWindow()
        self.sceneWindowBase = SceneWindowBase()
        self.consoleWindow = ConsoleWindow()
        self.propertyWindow = QWidget()

        self.labelPropertyWindow = LabelPropertyWindow()
        self.sliderPropertyWindow = SliderPropertyWindow()
        self.propertyWindowList = [self.labelPropertyWindow, self.sliderPropertyWindow]

        self.windowCenterWidget = QWidget()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.resize(1430, 800)
        self.setWindowTitle('PyPlay')
        self.setCentralWidget(self.windowCenterWidget)

    def initWidgets(self):
        self.labelPropertyWindow.hide()
        self.sliderPropertyWindow.hide()
        
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
        self.centerSplitter.setSizes([550, 250])

        self.allSplitter.addWidget(self.leftSplitter)
        self.allSplitter.addWidget(self.centerSplitter)
        self.allSplitter.addWidget(self.rightTab)
        self.allSplitter.setSizes([280, 800, 350])

    def initSignals(self):
        self.itemWindow.addSignal.connect(self.sceneWindow.add)
        self.itemWindow.deleteSignal.connect(self.sceneWindow.delete)
        self.itemWindow.clickSignal.connect(self.sceneWindow.focus)
        self.itemWindow.showPropertyWindowSignal.connect(self.sceneWindow.showPropertyWindow)
        self.itemWindow.deleteSignal.connect(self.hidePropertyWindow)

        self.sceneWindow.deleteSignal.connect(self.itemWindow.delete)
        self.sceneWindow.deleteSignal.connect(self.hidePropertyWindow)
        self.sceneWindow.clickSignal.connect(self.itemWindow.focus)
        self.sceneWindow.showPropertyWindowSignal.connect(self.showPropertyWindow)

        self.labelPropertyWindow.updateItemSignal.connect(self.sceneWindow.updateItemPropertiesOnScene)
        self.sliderPropertyWindow.updateItemSignal.connect(self.sceneWindow.updateItemPropertiesOnScene)

    def initLayouts(self):
        windowHLayout = QHBoxLayout(self.windowCenterWidget)
        windowHLayout.addWidget(self.allSplitter)

        sceneWindowHLayout = QHBoxLayout(self.sceneWindowBase)
        sceneWindowHLayout.addWidget(self.sceneWindow)

        propertyWindowVLayout = QVBoxLayout(self.propertyWindow)
        propertyWindowVLayout.addWidget(self.labelPropertyWindow)
        propertyWindowVLayout.addWidget(self.sliderPropertyWindow)

    def showPropertyWindow(self, propertyDict):
        for pw in self.propertyWindowList:
            pw.hide()

        if propertyDict['type'] == 'Label':
            self.labelPropertyWindow.show()
            self.labelPropertyWindow.setPropertyWindowValues(propertyDict)

        elif propertyDict['type'] == 'Slider':
            self.sliderPropertyWindow.show()
            self.sliderPropertyWindow.setPropertyWindowValues(propertyDict)

    def hidePropertyWindow(self):
        scene = self.sceneWindow.currentScene()
        for item in scene.items():
            # 这里循环所有属性窗口
            # 如果有一样的UUID，说明当点点击的项没有被删除
            # 如果项被删除了的话，那么肯定是匹配不到UUID的
            if self.labelPropertyWindow.UUID == item.UUID:
                break
        else:
            self.labelPropertyWindow.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    playWindow = PlayWindow()
    playWindow.setStyleSheet(readQss('default.qss'))
    playWindow.show()
    sys.exit(app.exec())
