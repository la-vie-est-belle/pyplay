import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AssetWindow(QWidget):
    newFolderSignal = pyqtSignal(str)
    newFileSignal = pyqtSignal(str)
    deleteSignal = pyqtSignal(str)
    pathSignal = pyqtSignal(str)

    def __init__(self):
        super(QWidget, self).__init__()

        self.projectTreeView = QTreeView()
        self.projectDirModel = QFileSystemModel()
        self.projectPath = '/Users/louis/Desktop/pyplay'
        self.contextMenu = AssetWidnowContextMenu(self)

        self.currentIndex = None

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.setWindowTitle('资源管理器')

    def initWidgets(self):
        # Show the current project directory.
        index = self.projectDirModel.setRootPath(self.projectPath)
        self.projectTreeView.setModel(self.projectDirModel)
        self.projectTreeView.setRootIndex(index)
        self.projectTreeView.setExpandsOnDoubleClick(True)

        # Only need to show file(folder) name.
        self.projectTreeView.setColumnHidden(1, True)
        self.projectTreeView.setColumnHidden(2, True)
        self.projectTreeView.setColumnHidden(3, True)

        # Don't want to show the header.
        self.projectTreeView.setHeaderHidden(True)

    def initSignals(self):
        self.pathSignal.connect(self.setProjectPath)
        self.projectTreeView.doubleClicked.connect(self.openFile)

    def initLayouts(self):
        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(self.projectTreeView)

    """Slots"""

    def openFile(self, modelIndex):
        path = self.projectDirModel.filePath(modelIndex)
        if os.path.isfile(path):
            print('打开')

    def setProjectPath(self, path):
        self.projectPath = path

    """Events"""
    def contextMenuEvent(self, event):
        self.contextMenu.exec(event.globalPos())

        # index = self.projectTreeView.indexAt(event.pos())

        # # User clicks on the blank
        # if not index.isValid():
        #     self.contextMenu.showContextMenuForBlank(event.globalPos())
        #     return

        # filePath = self.projectDirModel.filePath(index)
        # print(filePath)
        # # User clicks on the folder
        # if os.path.isdir(filePath):
        #     print(1)
        #     self.contextMenu.showContextMenuForFolder(event.globalPos())
        # # User clicks on the file
        # else:
        #     print(2)
        #     self.contextMenu.showContextMenuForFile(event.globalPos())

    def mousePressEvent(self, event):
        # if event.button() == Qt.RightButton:
        #     index = self.indexAt(event.pos())
        #
        #     if index.isValid():
        #         print(1)
        #     else:
        #         print(2)
        ...


class AssetWidnowContextMenu(QMenu):
    def __init__(self, parent):
        super(AssetWidnowContextMenu, self).__init__(parent=parent)
        """Submenu"""
        self.newFileMenu = QMenu(self)
        self.newFileMenu.setTitle('新建文件')

        """Action"""
        # Submenu Actions
        self.newTxtFileAction = QAction('新建txt文件', self.newFileMenu)
        self.newPythonFileAction = QAction('新建Py文件', self.newFileMenu)
        self.newJsonFileAction = QAction('新建JSON文件', self.newFileMenu)

        # Main menu Actions
        self.newFolderAction = QAction('新建文件夹', self)
        self.renameAction = QAction('重命名', self)
        self.deleteAction = QAction('删除', self)
        self.pasteAction = QAction('粘贴', self)
        self.copyAction = QAction('复制', self)
        self.cutAction = QAction('剪切', self)

        self.main()

    def main(self):
        self.addSubmenu()
        self.addSubmenuActions()
        self.addMainMenuActions()

    def addSubmenu(self):
        self.addMenu(self.newFileMenu)

    def addSubmenuActions(self):
        self.newFileMenu.addAction(self.newTxtFileAction)
        self.newFileMenu.addAction(self.newPythonFileAction)
        self.newFileMenu.addAction(self.newJsonFileAction)

    def addMainMenuActions(self):
        self.addAction(self.newFolderAction)
        self.addAction(self.renameAction)
        self.addAction(self.deleteAction)
        self.addAction(self.pasteAction)
        self.addAction(self.copyAction)
        self.addAction(self.cutAction)

    def showContextMenu(self):
        # 在这里检查是否action enabled
        ...


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = AssetWindow()
    assetWindow.show()
    sys.exit(app.exec())
