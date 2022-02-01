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
        self.contextMenu = ContextMenuForAssetWidnow(self)

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
        index = self.projectTreeView.indexAt(event.pos())

        # User clicks on the blank
        if not index.isValid():
            self.contextMenu.execBlankMainMenu(event.globalPos())
            return

        filePath = self.projectDirModel.filePath(index)
        # User clicks on the folder
        if os.path.isdir(filePath):
            self.contextMenu.execFolderMainMenu(event.globalPos())
        # User clicks on the file
        else:
            self.contextMenu.execFileMainMenu(event.globalPos())

    def mousePressEvent(self, event):
        # if event.button() == Qt.RightButton:
        #     index = self.indexAt(event.pos())
        #
        #     if index.isValid():
        #         print(1)
        #     else:
        #         print(2)
        ...


class ContextMenuForAssetWidnow(QObject):
    def __init__(self, parent):
        super(ContextMenuForAssetWidnow, self).__init__(parent=parent)
        """Menu"""
        # Main Menu
        self.fileMainMenu = QMenu()
        self.folderMainMenu = QMenu()
        self.blankMainMenu = QMenu()

        # Submenu
        self.newFileSubmenu = QMenu()
        self.newFileSubmenu.setTitle('新建文件')

        """Action"""
        # Main menu Actions
        self.newFolderAction = QAction('新建文件夹', self)
        self.renameAction = QAction('重命名', self)
        self.deleteAction = QAction('删除', self)
        self.pasteAction = QAction('粘贴', self)
        self.copyAction = QAction('复制', self)
        self.cutAction = QAction('剪切', self)

        # Submenu Actions
        self.newTxtFileAction = QAction('新建txt文件', self.newFileSubmenu)
        self.newPythonFileAction = QAction('新建Py文件', self.newFileSubmenu)
        self.newJsonFileAction = QAction('新建JSON文件', self.newFileSubmenu)

        self.main()

    def main(self):
        self.addSubmenuActions()
        self.setFileMainMenu()
        self.setFolderMainMenu()
        self.setBlankMainMenu()

    def addSubmenuActions(self):
        self.newFileSubmenu.addAction(self.newTxtFileAction)
        self.newFileSubmenu.addAction(self.newPythonFileAction)
        self.newFileSubmenu.addAction(self.newJsonFileAction)

    def setFileMainMenu(self):
        submenuList = [self.newFileSubmenu]
        actionList = [self.newFolderAction, self.renameAction, self.deleteAction,
                      self.copyAction, self.pasteAction, self.cutAction]

        for submenu in submenuList:
            self.fileMainMenu.addMenu(submenu)

        for action in actionList:
            self.fileMainMenu.addAction(action)

    def setFolderMainMenu(self):
        submenuList = [self.newFileSubmenu]
        actionList = [self.newFolderAction, self.renameAction, self.deleteAction,
                      self.copyAction, self.pasteAction, self.cutAction]

        for submenu in submenuList:
            self.folderMainMenu.addMenu(submenu)

        for action in actionList:
            self.folderMainMenu.addAction(action)

    def setBlankMainMenu(self):
        submenuList = [self.newFileSubmenu]
        actionList = [self.newFolderAction, self.copyAction, self.pasteAction]

        for submenu in submenuList:
            self.blankMainMenu.addMenu(submenu)

        for action in actionList:
            self.blankMainMenu.addAction(action)

    def execFileMainMenu(self, pos):
        # 在这里检查是否action enabled
        self.folderMainMenu.exec(pos)

    def execFolderMainMenu(self, pos):
        # 在这里检查是否action enabled
        self.folderMainMenu.exec(pos)

    def execBlankMainMenu(self, pos):
        # 在这里检查是否action enabled
        self.blankMainMenu.exec(pos)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = AssetWindow()
    assetWindow.show()
    sys.exit(app.exec())
