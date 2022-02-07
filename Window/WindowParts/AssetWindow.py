import re
import sys
import shutil
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AssetWindow(QWidget):
    pathSignal = pyqtSignal(str)

    def __init__(self):
        super(QWidget, self).__init__()
        self.searchLine = QLineEdit()
        self.searchListView = ListView()
        self.projectTreeView = TreeView()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.setWindowTitle('资源管理器')

    def initWidgets(self):
        # Search line
        self.searchLine.setPlaceholderText('搜索资源名称')
        # List view
        self.searchListView.hide()

    def initSignals(self):
        self.pathSignal.connect(self.setProjectPath)
        self.searchLine.textChanged.connect(self.search)

    def initLayouts(self):
        vLayout = QVBoxLayout(self)
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.searchLine)
        vLayout.addWidget(self.searchListView)
        vLayout.addWidget(self.projectTreeView)

    """Slots"""
    def setProjectPath(self, path):
        self.projectTreeView.setProjectPath(path)

    def search(self, s):
        if s:
            fileNameList = []
            it = QDirIterator(self.projectTreeView.projectPath, QDir.Dirs | QDir.NoDotAndDotDot | QDir.Files, QDirIterator.Subdirectories)
            while it.hasNext():
                it.next()
                if Path(it.filePath()).is_file() and re.search(f'{s}', it.fileName(), re.IGNORECASE):
                    fileNameList.append(it.fileName())

            self.searchListView.stringListModel.setStringList(fileNameList)
            self.projectTreeView.hide()
            self.searchListView.show()
        else:
            self.searchListView.hide()
            self.projectTreeView.show()

        self.update()


class ListView(QListView):
    # 加一个List View Delegate用来显示更详细的搜索结果
    def __init__(self):
        super(ListView, self).__init__()
        self.stringListModel = QStringListModel()

        self.main()

    def main(self):
        self.initWidgets()
        self.initSignals()

    def initWidgets(self):
        self.setModel(self.stringListModel)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def initSignals(self):
        self.doubleClicked.connect(self.openFile)

    """Slots"""
    def openFile(self, modelIndex):
        print(modelIndex.data())


class TreeView(QTreeView):
    def __init__(self):
        super(TreeView, self).__init__()
        self.copyOrCut = None
        self.clickedIndex = None
        self.cutIndexSet = set()
        self.projectPath = '/Users/louis/Desktop/pyplay'

        self.fileSystemModel = QFileSystemModel()
        self.clipboard = QApplication.clipboard()
        self.contextMenu = ContextMenuForTreeView(self, self.clipboard)
        self.treeViewDelegate = TreeViewDelegate(self.cutIndexSet)

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()

    def initWindowAttrs(self):
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initWidgets(self):
        # Show the current project directory.
        index = self.fileSystemModel.setRootPath(self.projectPath)
        self.setModel(self.fileSystemModel)
        self.setRootIndex(index)
        self.setItemDelegate(self.treeViewDelegate)

        # Only need to show file(folder) name.
        self.setHeaderHidden(True)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)

    def initSignals(self):
        # self.pathSignal.connect(self.setProjectPath)
        self.doubleClicked.connect(self.openFile)
        self.clicked.connect(lambda: self.fileSystemModel.setReadOnly(True))

        self.contextMenu.openSignal.connect(lambda: self.openFile(self.clickedIndex))
        self.contextMenu.newFolderSignal.connect(self.createNewFolder)
        self.contextMenu.renameSignal.connect(self.rename)
        self.contextMenu.deleteSignal.connect(self.delete)
        self.contextMenu.copySignal.connect(self.copy)
        self.contextMenu.cutSignal.connect(self.cut)
        self.contextMenu.pasteSignal.connect(self.paste)
        self.contextMenu.newFileSignal.connect(self.createNewFile)

    """Slots"""
    def setPtrojectPath(self, path):
        self.fileSystemModel.setRootPath(path)

    def openFile(self, modelIndex):
        path = Path(self.fileSystemModel.filePath(modelIndex))
        if path.is_file():
            print('打开')

        # 获取编辑器的可执行文件路径
        # 如果没有设置，则抛出提示

    def createNewFile(self, ext):
        fileName, ok = QInputDialog.getText(self, '新建文件夹', '请输入文件夹名称')
        if not ok:
            return

        # If user clicks at the blank area, selectedPath will be None.
        # This is one way to exec different context menus.
        selectedPath = self.fileSystemModel.filePath(self.clickedIndex)
        path = Path(selectedPath) if selectedPath else Path(self.projectPath)
        path = path if path.is_dir() else path.parent

        if (path / f'{fileName}{ext}').exists():
            QMessageBox.critical(self, '错误', '文件已存在')
            return

        (path / f'{fileName}{ext}').touch()
        self.update()

    def createNewFolder(self):
        folderName, ok = QInputDialog.getText(self, '新建文件夹', '请输入文件夹名称')
        if not ok:
            return

        selectedPath = self.fileSystemModel.filePath(self.clickedIndex)
        path = Path(selectedPath) if selectedPath else Path(self.projectPath)
        path = path if path.is_dir() else path.parent

        if (path / folderName).exists():
            QMessageBox.critical(self, '错误', '文件夹已存在')
            return

        (path / folderName).mkdir()
        self.update()

    def delete(self):
        choice = QMessageBox.question(self, '删除', '确定要删除吗？', QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            for modelIndex in self.selectedIndexes():
                path = Path(self.fileSystemModel.filePath(modelIndex))
                path.rmdir() if path.is_dir() else path.unlink()

        self.update()

    def rename(self):
        self.fileSystemModel.setReadOnly(False)
        self.edit(self.clickedIndex)

    def copy(self):
        urlList = []
        self.cutIndexSet.clear()
        for modelIndex in self.selectedIndexes():
            urlList.append(QUrl(self.fileSystemModel.filePath(modelIndex)))

        data = QMimeData()
        data.setUrls(urlList)
        self.clipboard.setMimeData(data)
        self.copyOrCut = 'copy'

    def cut(self):
        urlList = []
        self.cutIndexSet.clear()
        for modelIndex in self.selectedIndexes():
            urlList.append(QUrl(self.fileSystemModel.filePath(modelIndex)))
            self.cutIndexSet.add(modelIndex)
        self.clearSelection()

        data = QMimeData()
        data.setUrls(urlList)
        self.clipboard.setMimeData(data)
        self.copyOrCut = 'cut'

    def paste(self):
        data = self.clipboard.mimeData()
        if not data.urls():
            return

        for url in data.urls():
            fileOrFolderPath = Path(url.toString().replace('file://', ''))
            fileOrFolderName = fileOrFolderPath.name

            selectedPath = self.fileSystemModel.filePath(self.clickedIndex)
            destPath = Path(selectedPath) if selectedPath else Path(self.projectPath)
            destPath = destPath if destPath.is_dir() else destPath.parent

            # Check if the file or folder exists in the destPath.
            if (destPath / fileOrFolderName).exists():
                if fileOrFolderPath.is_dir():
                    QMessageBox.critical(self, '已存在', f'该目录下已存在文件夹{fileOrFolderName}！', QMessageBox.Ok)
                    continue
                else:
                    choice = QMessageBox.question(self, '文件已存在', f'该目录下已存在{fileOrFolderName}，是否覆盖？', QMessageBox.Yes | QMessageBox.No)
                    if choice == QMessageBox.Yes:
                        fileOrFolderPath.replace((destPath / fileOrFolderName))

            else:
                if self.copyOrCut == 'cut':
                    fileOrFolderPath.replace((destPath / fileOrFolderName))
                else:
                    # pathlib doesn't have copy function.
                    shutil.copyfile(str(fileOrFolderPath), str(destPath / fileOrFolderName))

        self.update()

        if self.copyOrCut == 'cut':
            self.clipboard.clear()
            self.copyOrCut = None
            self.cutIndexSet.clear()

    """Events"""
    def contextMenuEvent(self, event):
        self.clickedIndex = self.indexAt(event.pos())

        # User clicks on the blank
        if not self.clickedIndex.isValid():
            self.contextMenu.execBlankMainMenu(event.globalPos())
            return

        # User clicks on the folder or the file
        path = Path(self.fileSystemModel.filePath(self.clickedIndex))
        if path.is_dir():
            self.contextMenu.execFolderMainMenu(event.globalPos())
        else:
            self.contextMenu.execFileMainMenu(event.globalPos())

    def dragEnterEvent(self, event):
        urlList = []
        for modelIndex in self.selectedIndexes():
            urlList.append(QUrl(QFileSystemModel().filePath(modelIndex)))

        event.mimeData().setUrls(urlList)
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        ...

    def dropEvent(self, event):
        data = event.mimeData()
        if not data.urls():
            return

        for url in data.urls():
            fileOrFolderPath = Path(url.toString().replace('file://', ''))
            fileOrFolderName = fileOrFolderPath.name

            selectedPath = self.fileSystemModel.filePath(self.indexAt(event.pos()))
            destPath = Path(selectedPath) if selectedPath else Path(self.projectPath)
            destPath = destPath if destPath.is_dir() else destPath.parent

            # Check if the file or folder exists in the destPath.
            if (destPath / fileOrFolderName).exists():
                if fileOrFolderPath.is_dir():
                    QMessageBox.critical(self, '已存在', f'该目录下已存在文件夹{fileOrFolderName}！', QMessageBox.Ok)
                    continue
                else:
                    choice = QMessageBox.question(self, '文件已存在', f'该目录下已存在{fileOrFolderName}，是否覆盖？', QMessageBox.Yes | QMessageBox.No)
                    if choice == QMessageBox.Yes:
                        fileOrFolderPath.replace((destPath / fileOrFolderName))

            else:
                fileOrFolderPath.replace((destPath / fileOrFolderName))

        self.update()


class TreeViewDelegate(QStyledItemDelegate):
    def __init__(self, cutIndexSet):
        super(TreeViewDelegate, self).__init__()
        self.cutIndexSet = cutIndexSet
        self.pen = QPen(QColor(0, 105, 217, 128))
        self.brush = QBrush(QColor(0, 105, 217, 128))

    def paint(self, painter, option, index):
        super(TreeViewDelegate, self).paint(painter, option, index)

        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        for cutIndex in self.cutIndexSet:
            if index == cutIndex:
                rect = option.rect
                painter.drawRect(rect.x()-100, rect.y(), rect.width()+100, rect.height())


class ContextMenuForTreeView(QObject):
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
        super(ContextMenuForTreeView, self).__init__(parent=parent)
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
        actionList = [self.newFolderAction, self.pasteAction]

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
