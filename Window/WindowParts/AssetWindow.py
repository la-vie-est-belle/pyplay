import os
import sys
import shutil
from PyQt5.QtGui import *
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
        self.clipboard = QApplication.clipboard()
        self.contextMenu = ContextMenuForAssetWindow(self, self.clipboard)

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
        # self.projectTreeView.setEditTriggers(QAbstractItemView.DoubleClicked)

        # Only need to show file(folder) name.
        self.projectTreeView.setColumnHidden(1, True)
        self.projectTreeView.setColumnHidden(2, True)
        self.projectTreeView.setColumnHidden(3, True)

        # Don't want to show the header.
        self.projectTreeView.setHeaderHidden(True)

        # Double click to edit. Should use this code to make it work.
        # self.projectDirModel.setReadOnly(False)

    def initSignals(self):
        self.pathSignal.connect(self.setProjectPath)
        self.projectTreeView.doubleClicked.connect(self.openFile)
        self.projectTreeView.clicked.connect(lambda: self.projectDirModel.setReadOnly(True))

        self.contextMenu.openSignal.connect(lambda: self.openFile(self.currentIndex))
        self.contextMenu.newFolderSignal.connect(self.createNewFolder)
        self.contextMenu.renameSignal.connect(self.renameFileOrFolder)
        self.contextMenu.deleteSignal.connect(self.deleteFileOrFolder)
        self.contextMenu.copySignal.connect(self.copyFileOrFolder)
        self.contextMenu.cutSignal.connect(self.cutFileOrFolder)
        self.contextMenu.pasteSignal.connect(self.pasteFileOrFolderForCut)
        self.contextMenu.newFileSignal.connect(self.createNewFile)

    def initLayouts(self):
        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(self.projectTreeView)

    """Slots"""
    def openFile(self, modelIndex):
        path = self.projectDirModel.filePath(modelIndex)
        if os.path.isfile(path):
            print('打开')

        # 获取编辑器的可执行文件路径
        # 如果没有设置，则抛出提示

    def setProjectPath(self, path):
        self.projectPath = path

    def createNewFile(self, ext):
        fileName, ok = QInputDialog.getText(self, '新建文件夹', '请输入文件夹名称')
        if not ok:
            return

        selectedPath = self.projectDirModel.filePath(self.currentIndex)
        path = selectedPath if selectedPath else self.projectPath

        if os.path.exists(os.path.join(path, f'{fileName}{ext}')):
            QMessageBox.critical(self, '错误', '文件已存在')
            return

        if os.path.isdir(path):
            with open(os.path.join(path, f'{fileName}{ext}'), 'w'): ...
        else:
            with open(os.path.join(os.path.dirname(path), f'{fileName}{ext}'), 'w'): ...

        self.update()

    def createNewFolder(self):
        folderName, ok = QInputDialog.getText(self, '新建文件夹', '请输入文件夹名称')
        if not ok:
            return

        selectedPath = self.projectDirModel.filePath(self.currentIndex)
        path = selectedPath if selectedPath else self.projectPath
        try:
            if os.path.isdir(path):
                os.mkdir(os.path.join(path, folderName))
            else:
                os.mkdir(os.path.join(os.path.dirname(path), f'{folderName}'))

            self.update()
        except FileExistsError:
            QMessageBox.critical(self, '错误', '文件夹已存在')

    def deleteFileOrFolder(self):
        choice = QMessageBox.question(self, '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)  # 1

        if choice == QMessageBox.Yes:
            self.projectDirModel.remove(self.currentIndex)

        self.update()

    def renameFileOrFolder(self):
        self.projectDirModel.setReadOnly(False)
        self.projectTreeView.edit(self.currentIndex)

    def copyFileOrFolder(self):
        path = self.projectDirModel.filePath(self.currentIndex)
        self.clipboard.setText(path)

    def cutFileOrFolder(self):
        path = self.projectDirModel.filePath(self.currentIndex)
        self.clipboard.setText(path)

    def pasteFileOrFolderForCut(self):
        fileOrFolderPath = self.clipboard.text()
        fileOrFolderName = os.path.basename(fileOrFolderPath)
        selectedPath = self.projectDirModel.filePath(self.currentIndex)
        destPath = selectedPath if selectedPath else self.projectPath

        # Check if the destPath already has a file or a folder with same name.
        if os.path.exists(os.path.join(destPath, fileOrFolderName)):
            QMessageBox.critical(self, '错误', '文件（夹）已存在')
            return

        if os.path.isdir(destPath):
            shutil.move(fileOrFolderPath, destPath)
        else:
            shutil.move(fileOrFolderPath, os.path.dirname(destPath))

        self.update()
        self.clipboard.clear()

    """Events"""
    def contextMenuEvent(self, event):
        index = self.projectTreeView.indexAt(event.pos())
        self.currentIndex = index

        # User clicks on the blank
        if not index.isValid():
            self.contextMenu.execBlankMainMenu(event.globalPos())
            return

        # User clicks on the folder or the file
        filePath = self.projectDirModel.filePath(index)
        if os.path.isdir(filePath):
            self.contextMenu.execFolderMainMenu(event.globalPos())
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

    def closeEvent(self, event):
        self.clipboard.clear()


class ContextMenuForAssetWindow(QObject):
    # Signals for Main Menu Actions
    openSignal = pyqtSignal()
    newFolderSignal = pyqtSignal()
    renameSignal = pyqtSignal()
    deleteSignal = pyqtSignal()
    pasteSignal = pyqtSignal()
    copySignal = pyqtSignal()
    cutSignal = pyqtSignal()

    # Signals for Submenu Actions
    newFileSignal = pyqtSignal(str)

    def __init__(self, parent, clipboard):
        super(ContextMenuForAssetWindow, self).__init__(parent=parent)
        self.clipboard = clipboard

        # Main Menu
        self.fileMainMenu = QMenu()
        self.folderMainMenu = QMenu()
        self.blankMainMenu = QMenu()

        # Submenu
        self.newFileSubmenu = QMenu()
        self.newFileSubmenu.setTitle('新建文件')

        # Main Menu Actions
        self.openAction = QAction('打开', self)
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
        self.initSignals()
        self.addSubmenuActions()
        self.setFileMainMenu()
        self.setFolderMainMenu()
        self.setBlankMainMenu()

    def initSignals(self):
        self.openAction.triggered.connect(self.openSignal.emit)
        self.newFolderAction.triggered.connect(self.newFolderSignal.emit)
        self.renameAction.triggered.connect(self.renameSignal.emit)
        self.deleteAction.triggered.connect(self.deleteSignal.emit)
        self.pasteAction.triggered.connect(self.pasteSignal.emit)
        self.copyAction.triggered.connect(self.copySignal.emit)
        self.cutAction.triggered.connect(self.cutSignal.emit)

        self.newTxtFileAction.triggered.connect(lambda: self.newFileSignal.emit('.txt'))
        self.newPythonFileAction.triggered.connect(lambda: self.newFileSignal.emit('.py'))
        self.newJsonFileAction.triggered.connect(lambda: self.newFileSignal.emit('.json'))

    def addSubmenuActions(self):
        self.newFileSubmenu.addAction(self.newTxtFileAction)
        self.newFileSubmenu.addAction(self.newPythonFileAction)
        self.newFileSubmenu.addAction(self.newJsonFileAction)

    def setFileMainMenu(self):
        submenuList = [self.newFileSubmenu]
        actionList = [self.newFolderAction, self.openAction, self.renameAction,
                      self.deleteAction, self.copyAction, self.pasteAction, self.cutAction]

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
        if not self.clipboard.text():
            self.pasteAction.setEnabled(False)
        else:
            self.pasteAction.setEnabled(True)

        self.fileMainMenu.exec(pos)

    def execFolderMainMenu(self, pos):
        if not self.clipboard.text():
            self.pasteAction.setEnabled(False)
        else:
            self.pasteAction.setEnabled(True)

        self.folderMainMenu.exec(pos)

    def execBlankMainMenu(self, pos):
        if not self.clipboard.text():
            self.pasteAction.setEnabled(False)
        else:
            self.pasteAction.setEnabled(True)

        self.blankMainMenu.exec(pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = AssetWindow()
    assetWindow.show()
    sys.exit(app.exec())
