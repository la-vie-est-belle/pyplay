import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AssetWindow(QWidget):
    newFolderSignal = pyqtSignal(str)
    newFileSignal = pyqtSignal(str)
    deleteSignal = pyqtSignal(str)
    pathSignal = pyqtSignal(str)

    def __init__(self):
        super(AssetWindow, self).__init__()
        self._projectDirModel = QFileSystemModel()
        self._projectTreeView = QTreeView(self)
        self._projectPath = '/Users/louis/Desktop/pyplay'
        self._contextMenu = ContextMenu(self)

        self._main()

    def _main(self):
        self._initWidgets()
        self._initSignals()
        self._initLayouts()

    def _initWidgets(self):
        # Show the current project directory.
        index = self._projectDirModel.setRootPath(self._projectPath)
        self._projectTreeView.setModel(self._projectDirModel)
        self._projectTreeView.setRootIndex(index)

        # Only need to show file(folder) name.
        self._projectTreeView.setColumnHidden(1, True)
        self._projectTreeView.setColumnHidden(2, True)
        self._projectTreeView.setColumnHidden(3, True)

        # Don't want to show the header.
        self._projectTreeView.setHeaderHidden(True)

    def _initSignals(self):
        self.pathSignal.connect(self._setProjectPath)

    def _initLayouts(self):
        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self._projectTreeView)

    """Slots"""
    def _setProjectPath(self, path):
        self._projectPath = path

    """Events"""
    def contextMenuEvent(self, event):
        self._contextMenu.exec(event.globalPos())


class ContextMenu(QMenu):
    def __init__(self, parent):
        super(ContextMenu, self).__init__(parent=parent)
        newFileMenu = QMenu(self)
        newFileMenu.setTitle('新建文件')
        newTxtFileAction = QAction('新建txt文件', newFileMenu)
        newPythonFileAction = QAction('新建Py文件', newFileMenu)
        newJsonFileAction = QAction('新建JSON文件', newFileMenu)
        newFileMenu.addAction(newTxtFileAction)
        newFileMenu.addAction(newPythonFileAction)
        newFileMenu.addAction(newJsonFileAction)

        newFolderAction = QAction('新建文件夹', self)
        deleteAction = QAction('删除', self)
        self.addAction(newFolderAction)
        self.addMenu(newFileMenu)
        self.addAction(deleteAction)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = AssetWindow()
    assetWindow.show()
    sys.exit(app.exec())
