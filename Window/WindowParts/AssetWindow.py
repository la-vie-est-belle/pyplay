import os
import sys
import shutil
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TreeViewDelegate(QStyledItemDelegate):
    def __init__(self, cutIndexSet):
        super(TreeViewDelegate, self).__init__()
        self.cutIndexSet = cutIndexSet

    def paint(self, painter, option, index):
        super(TreeViewDelegate, self).paint(painter, option, index)
        painter.setPen(QColor(0, 105, 217, 128))
        painter.setBrush(QColor(0, 105, 217, 128))

        for cutIndex in self.cutIndexSet:
            if index == cutIndex:
                rect = option.rect
                painter.drawRect(rect.x()-100, rect.y(), rect.width()+100, rect.height())


class AssetWindow(QWidget):
    newFolderSignal = pyqtSignal(str)
    newFileSignal = pyqtSignal(str)
    deleteSignal = pyqtSignal(str)
    pathSignal = pyqtSignal(str)

    def __init__(self):
        super(QWidget, self).__init__()
        self.searchLine = QLineEdit()
        self.projectTreeView = QTreeView()
        self.projectDirModel = QFileSystemModel()
        self.projectPath = '/Users/louis/Desktop/pyplay'

        self.currentIndex = None
        self.copyOrCut = None
        self.cutIndexSet = set()

        self.clipboard = QApplication.clipboard()
        self.contextMenu = ContextMenuForAssetWindow(self, self.clipboard)
        self.treeViewDelegate = TreeViewDelegate(self.cutIndexSet)

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.setWindowTitle('资源管理器')

    def initWidgets(self):
        # Search Line
        self.searchLine.setPlaceholderText('搜索资源名称')

        # Show the current project directory.
        index = self.projectDirModel.setRootPath(self.projectPath)
        self.projectTreeView.setModel(self.projectDirModel)
        self.projectTreeView.setRootIndex(index)
        self.projectTreeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.projectTreeView.setItemDelegate(self.treeViewDelegate)

        # Only need to show file(folder) name.
        self.projectTreeView.setColumnHidden(1, True)
        self.projectTreeView.setColumnHidden(2, True)
        self.projectTreeView.setColumnHidden(3, True)

        # Don't want to show the header.
        self.projectTreeView.setHeaderHidden(True)

    def initSignals(self):
        self.pathSignal.connect(self.setProjectPath)
        self.projectTreeView.doubleClicked.connect(self.openFile)
        self.projectTreeView.clicked.connect(lambda: self.projectDirModel.setReadOnly(True))

        self.contextMenu.openSignal.connect(lambda: self.openFile(self.currentIndex))
        self.contextMenu.newFolderSignal.connect(self.createNewFolder)
        self.contextMenu.renameSignal.connect(self.rename)
        self.contextMenu.deleteSignal.connect(self.delete)
        self.contextMenu.copySignal.connect(self.copy)
        self.contextMenu.cutSignal.connect(self.cut)
        self.contextMenu.pasteSignal.connect(self.paste)
        self.contextMenu.newFileSignal.connect(self.createNewFile)

    def initLayouts(self):
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        # vLayout.addWidget(self.searchLine)
        vLayout.addWidget(self.projectTreeView)

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
        path = path if os.path.isdir(path) else os.path.dirname(path)

        if os.path.exists(os.path.join(path, f'{fileName}{ext}')):
            QMessageBox.critical(self, '错误', '文件已存在')
            return

        with open(os.path.join(path, f'{fileName}{ext}'), 'w'):
            ...

        self.update()

    def createNewFolder(self):
        folderName, ok = QInputDialog.getText(self, '新建文件夹', '请输入文件夹名称')
        if not ok:
            return

        selectedPath = self.projectDirModel.filePath(self.currentIndex)
        path = selectedPath if selectedPath else self.projectPath
        path = path if os.path.isdir(path) else os.path.dirname(path)
        try:
            os.mkdir(os.path.join(path, folderName))
            self.update()
        except FileExistsError:
            QMessageBox.critical(self, '错误', '文件夹已存在')

    def delete(self):
        choice = QMessageBox.question(self, '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)  # 1

        if choice == QMessageBox.Yes:
            for modeIndex in self.projectTreeView.selectedIndexes():
                self.projectDirModel.remove(modeIndex)

        self.update()

    def rename(self):
        self.projectDirModel.setReadOnly(False)
        self.projectTreeView.edit(self.currentIndex)

    def copy(self):
        urlList = []
        self.cutIndexSet.clear()
        for modelIndex in self.projectTreeView.selectedIndexes():
            urlList.append(QUrl(self.projectDirModel.filePath(modelIndex)))

        data = QMimeData()
        data.setUrls(urlList)
        self.clipboard.setMimeData(data)
        self.copyOrCut = 'copy'

    def cut(self):
        urlList = []
        self.cutIndexSet.clear()
        for modelIndex in self.projectTreeView.selectedIndexes():
            urlList.append(QUrl(self.projectDirModel.filePath(modelIndex)))
            self.cutIndexSet.add(modelIndex)
        self.projectTreeView.clearSelection()

        data = QMimeData()
        data.setUrls(urlList)
        self.clipboard.setMimeData(data)
        self.copyOrCut = 'cut'

    def paste(self):
        data = self.clipboard.mimeData()
        if not data.urls():
            return

        for url in data.urls():
            fileOrFolderPath = url.toString().replace('file://', '')
            fileOrFolderName = os.path.basename(fileOrFolderPath)

            selectedPath = self.projectDirModel.filePath(self.currentIndex)
            destPath = selectedPath if selectedPath else self.projectPath
            destPath = destPath if os.path.isdir(destPath) else os.path.dirname(destPath)

            # Check if the file or folder exists in the destPath.
            if os.path.exists(os.path.join(destPath, fileOrFolderName)):
                if os.path.isdir(fileOrFolderPath):
                    QMessageBox.critical(self, '已存在', f'该目录下已存在文件夹{fileOrFolderName}！', QMessageBox.Ok)
                    continue
                else:
                    choice = QMessageBox.question(self, '文件已存在', f'该目录下已存在{fileOrFolderName}，是否覆盖？', QMessageBox.Yes | QMessageBox.No)  # 1

                    if choice == QMessageBox.No:
                        continue

                    if self.copyOrCut == 'cut':
                        shutil.move(fileOrFolderPath, os.path.join(destPath, fileOrFolderName))
                    else:
                        shutil.copyfile(fileOrFolderPath, os.path.join(destPath, fileOrFolderName))
            else:
                if self.copyOrCut == 'cut':
                    shutil.move(fileOrFolderPath, destPath)
                else:
                    if os.path.isdir(fileOrFolderPath):
                        shutil.copytree(fileOrFolderPath, os.path.join(destPath, fileOrFolderName))
                    else:
                        shutil.copyfile(fileOrFolderPath, os.path.join(destPath, fileOrFolderName))

        self.update()

        if self.copyOrCut == 'cut':
            self.clipboard.clear()
            self.copyOrCut = None
            self.cutIndexSet.clear()

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

    def keyPressEvent(self, event):
        ...

    # def paintEvent(self, event):
    #     super(AssetWindow, self).paintEvent(event)
    #     if not self.cutRectList:
    #         return
    #
    #     print(111)
    #     painter = QPainter(self)
    #     painter.setPen(QColor(128, 128, 255, 128))
    #     painter.setBrush(QColor(128, 128, 255, 128))
    #     for rect in self.cutRectList:
    #         painter.drawRect(rect)
    #
    #     # self.update()


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
