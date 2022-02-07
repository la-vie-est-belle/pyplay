import re
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ItemWindow(QWidget):
    def __init__(self):
        super(ItemWindow, self).__init__()
        self.searchLine = QLineEdit()
        self.itemTreeView = TreeView()
        self.searchListView = ListView()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()
        self.initLayouts()

    def initWindowAttrs(self):
        self.setWindowTitle('层级窗口')

    def initWidgets(self):
        self.searchLine.setPlaceholderText('搜索项')
        self.searchListView.hide()

    def initSignals(self):
        self.searchLine.textChanged.connect(self.search)

    def initLayouts(self):
        vLayout = QVBoxLayout(self)
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.addWidget(self.searchLine)
        vLayout.addWidget(self.itemTreeView)
        vLayout.addWidget(self.searchListView)

    """Slots"""
    def search(self, s):
        s = s.strip()
        searchResult = []
        if s:
            treeViewStandardItemModel = self.itemTreeView.standardItemModel
            for row in range(treeViewStandardItemModel.rowCount()):
                item = treeViewStandardItemModel.item(row, 0)
                if re.search(f'{s}', item.text(), re.I):
                    searchResult.append(item)
                self.searchRecursively(s, searchResult, item)

            listViewStandardItemModel = self.searchListView.standardItemModel
            listViewStandardItemModel.setRowCount(0)
            for item in searchResult:
                listViewStandardItemModel.appendRow(QStandardItem(item))    # 如果是实例化的话，考虑下后面点击显示属性窗口会不会有问题

            self.itemTreeView.hide()
            self.searchListView.show()

        else:
            self.searchListView.hide()
            self.itemTreeView.show()

    def searchRecursively(self, keyword, storageList, parentItem):
        if parentItem.hasChildren():
            for i in range(500):
                childItem = parentItem.child(i, 0)
                if childItem:
                    if re.search(f'{keyword}', childItem.text(), re.IGNORECASE):
                        storageList.append(childItem)
                    self.searchRecursively(keyword, storageList, childItem)
                else:
                    break


class TreeView(QTreeView):
    def __init__(self):
        super(TreeView, self).__init__()
        self.standardItemModel = QStandardItemModel()
        self.allItems = []
        self.copyOrCut = None
        self.clickedIndex = None
        self.cutIndexSet = set()
        self.dragItemIndexDict = {}
        self.copyOrCutItemIndexDict = {}

        self.contextMenu = ContextMenuForTreeView(self, self.copyOrCutItemIndexDict)
        self.treeViewDelegate = TreeViewDelegate(self.cutIndexSet)

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()

    def initWindowAttrs(self):
        self.setHeaderHidden(True)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initWidgets(self):
        # 新建场景默认有一个Canvas
        sceneItem = QStandardItem('Scene')
        self.standardItemModel.appendRow(sceneItem)
        item2 = QStandardItem('item')
        item3 = QStandardItem('item')
        sceneItem.appendRow(item2)
        item2.appendRow(item3)
        self.setModel(self.standardItemModel)
        self.setItemDelegate(self.treeViewDelegate)

        # print(self.standardItemModel.findItems('Camera', flags=Qt.MatchContains))

    def initSignals(self):
        self.clicked.connect(self.showProperty)

        self.contextMenu.renameSignal.connect(self.rename)
        self.contextMenu.deleteSignal.connect(self.delete)
        self.contextMenu.copySignal.connect(self.copy)
        self.contextMenu.cutSignal.connect(self.cut)
        self.contextMenu.pasteSignal.connect(self.paste)
        self.contextMenu.newItemSignal.connect(self.createNewItem)

    """Slots"""
    def showProperty(self, modelIndex):
        ...

    def rename(self):
        self.edit(self.clickedIndex)

    def delete(self):
        for modelIndex in self.selectedIndexes():
            item = self.standardItemModel.itemFromIndex(modelIndex)
            if item.parent():
                item.parent().removeRow(item.row())
            else:
                self.standardItemModel.removeRow(item.row())

    def copy(self):
        self.cutIndexSet.clear()
        self.copyOrCutItemIndexDict.clear()

        for modelIndex in self.selectedIndexes():
            print(modelIndex)
            parentItem = self.standardItemModel.itemFromIndex(modelIndex)
            self.getItemChildrenRecursively(self.copyOrCutItemIndexDict, modelIndex, parentItem)

        self.copyOrCut = 'copy'

    def cut(self):
        self.cutIndexSet.clear()
        self.copyOrCutItemIndexDict.clear()

        for modelIndex in self.selectedIndexes():
            parentItem = self.standardItemModel.itemFromIndex(modelIndex)
            self.getItemChildrenRecursively(self.copyOrCutItemIndexDict, modelIndex, parentItem)
            self.cutIndexSet.add(modelIndex)

        self.copyOrCut = 'cut'

    def getItemChildrenRecursively(self, itemStorageDict, modelIndex, parentItem):
        itemStorageDict[modelIndex] = []

        if parentItem.hasChildren():
            for i in range(500):
                childItem = parentItem.child(i, 0)
                if childItem:
                    childIndex = parentItem.child(i, 0).index()
                    itemStorageDict[modelIndex].append(childIndex)
                    self.getItemChildrenRecursively(itemStorageDict, childIndex, childItem)
                else:
                    break

    def paste(self):
        if self.clickedIndex.isValid():
            # The parent item can not be cut to its children.
            if self.copyOrCut == 'cut':
                for parentModelIndex, childModelIndexList in self.copyOrCutItemIndexDict.items():
                    if self.clickedIndex in childModelIndexList:
                        return

            currentClickItem = self.standardItemModel.itemFromIndex(self.clickedIndex)
            for parentModelIndex, childModelIndexList in self.copyOrCutItemIndexDict.items():
                parentItem = QStandardItem(self.standardItemModel.itemFromIndex(parentModelIndex))
                currentClickItem.appendRow(parentItem)
                if childModelIndexList:
                    self.pasteItemRecdursively(self.copyOrCutItemIndexDict, parentItem, childModelIndexList)
                break
        else:
            for parentModelIndex, childModelIndexList in self.copyOrCutItemIndexDict.items():
                parentItem = QStandardItem(self.standardItemModel.itemFromIndex(parentModelIndex))
                self.standardItemModel.appendRow(parentItem)
                if childModelIndexList:
                    self.pasteItemRecdursively(self.copyOrCutItemIndexDict, parentItem, childModelIndexList)
                break

        if self.copyOrCut == 'cut':
            for parentModelIndex in self.copyOrCutItemIndexDict.keys():
                item = self.standardItemModel.itemFromIndex(parentModelIndex)
                if item.parent():
                    item.parent().removeRow(item.row())
                else:
                    self.standardItemModel.removeRow(item.row())
                break

            self.copyOrCut = None
            self.cutIndexSet.clear()
            self.copyOrCutItemIndexDict.clear()

    def pasteItemRecdursively(self, itemStorageDict, parentItem, childModelIndexList):
        for childModelIndex in childModelIndexList:
            childItem = QStandardItem(self.standardItemModel.itemFromIndex(childModelIndex))
            parentItem.appendRow(childItem)
            if itemStorageDict.get(childModelIndex):
                self.pasteItemRecdursively(itemStorageDict, childItem, itemStorageDict[childModelIndex])

    def createNewItem(self, itemName):
        if itemName == 'QLabel':
            ...
        elif itemName == 'QPushButton':
            ...
        elif itemName == 'QLineEdit':
            ...

    """Events"""
    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        self.clickedIndex = index

        if index.isValid():
            self.contextMenu.execItemMainMenu(event.globalPos())
        else:
            self.contextMenu.execBlankMainMenu(event.globalPos())

    def dragEnterEvent(self, event):
        self.dragItemIndexDict = {}
        for modelIndex in self.selectedIndexes():
            parentItem = self.standardItemModel.itemFromIndex(modelIndex)
            self.getItemChildrenRecursively(self.dragItemIndexDict, modelIndex, parentItem)

        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        ...

    def dropEvent(self, event):
        if not self.dragItemIndexDict:
            return

        index = self.indexAt(event.pos())
        if index.isValid():
            for parentModelIndex, childModelIndexList in self.dragItemIndexDict.items():
                if index in childModelIndexList:
                    return

            targetItem = self.standardItemModel.itemFromIndex(index)
            for parentModelIndex, childModelIndexList in self.dragItemIndexDict.items():
                parentItem = QStandardItem(self.standardItemModel.itemFromIndex(parentModelIndex))
                targetItem.appendRow(parentItem)
                if childModelIndexList:
                    self.pasteItemRecdursively(self.dragItemIndexDict, parentItem, childModelIndexList)
                break
        else:
            for parentModelIndex, childModelIndexList in self.dragItemIndexDict.items():
                parentItem = QStandardItem(self.standardItemModel.itemFromIndex(parentModelIndex))
                self.standardItemModel.appendRow(parentItem)
                if childModelIndexList:
                    self.pasteItemRecdursively(self.dragItemIndexDict, parentItem, childModelIndexList)
                break

        for parentModelIndex in self.dragItemIndexDict.keys():
                item = self.standardItemModel.itemFromIndex(parentModelIndex)
                if item.parent():
                    item.parent().removeRow(item.row())
                else:
                    self.standardItemModel.removeRow(item.row())
                break

        self.dragItemIndexDict.clear()


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


class ListView(QListView):
    def __init__(self):
        super(ListView, self).__init__()
        self.standardItemModel = QStandardItemModel()

        self.main()

    def main(self):
        self.initWindowAttrs()
        self.initWidgets()
        self.initSignals()

    def initWindowAttrs(self):
        self.setModel(self.standardItemModel)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def initWidgets(self):
        ...

    def initSignals(self):
        self.clicked.connect(self.showProperty)

    def showProperty(self, index):
        print(index.data())


class ContextMenuForTreeView(QObject):
    # Signals for Main Menu Actions
    renameSignal = pyqtSignal()
    deleteSignal = pyqtSignal()
    pasteSignal = pyqtSignal()
    copySignal = pyqtSignal()
    cutSignal = pyqtSignal()

    # Signals for Submenu Actions
    newItemSignal = pyqtSignal(str)

    def __init__(self, parent, copyOrCutItemIndexDict):
        super(ContextMenuForTreeView, self).__init__(parent=parent)
        self.copyOrCutItemIndexDict = copyOrCutItemIndexDict

        # Main Menu
        self.itemMainMenu = QMenu()
        self.blankMainMenu = QMenu()

        # Submenu
        self.newItemSubmenu = QMenu()
        self.newItemSubmenu.setTitle('创建项')

        # Main Menu Actions
        self.renameAction = QAction('重命名', self)
        self.deleteAction = QAction('删除', self)
        self.pasteAction = QAction('粘贴', self)
        self.copyAction = QAction('复制', self)
        self.cutAction = QAction('剪切', self)

        # Submenu Actions
        self.newLabelAction = QAction('Label', self.newItemSubmenu)
        self.newButtonAction = QAction('Button', self.newItemSubmenu)
        self.newLineEditAction = QAction('LineEdit', self.newItemSubmenu)

        self.main()

    def main(self):
        self.initSignals()
        self.addSubmenuActions()
        self.setItemMainMenu()
        self.setBlankMainMenu()

    def initSignals(self):
        self.renameAction.triggered.connect(self.renameSignal.emit)
        self.deleteAction.triggered.connect(self.deleteSignal.emit)
        self.pasteAction.triggered.connect(self.pasteSignal.emit)
        self.copyAction.triggered.connect(self.copySignal.emit)
        self.cutAction.triggered.connect(self.cutSignal.emit)

        self.newLabelAction.triggered.connect(lambda: self.newItemSignal.emit('QLabel'))
        self.newButtonAction.triggered.connect(lambda: self.newItemSignal.emit('QPushButton'))
        self.newLineEditAction.triggered.connect(lambda: self.newItemSignal.emit('QLineEdit'))

    def addSubmenuActions(self):
        self.newItemSubmenu.addAction(self.newLabelAction)
        self.newItemSubmenu.addAction(self.newButtonAction)
        self.newItemSubmenu.addAction(self.newLineEditAction)

    def setItemMainMenu(self):
        submenuList = [self.newItemSubmenu]
        actionList = [self.renameAction, self.deleteAction, self.copyAction, self.pasteAction, self.cutAction]

        for submenu in submenuList:
            self.itemMainMenu.addMenu(submenu)

        for action in actionList:
            self.itemMainMenu.addAction(action)

    def setBlankMainMenu(self):
        submenuList = [self.newItemSubmenu]
        actionList = [self.pasteAction]

        for submenu in submenuList:
            self.blankMainMenu.addMenu(submenu)

        for action in actionList:
            self.blankMainMenu.addAction(action)

    def execItemMainMenu(self, pos):
        if not self.copyOrCutItemIndexDict:
            self.pasteAction.setEnabled(False)
        else:
            self.pasteAction.setEnabled(True)

        self.itemMainMenu.exec(pos)

    def execBlankMainMenu(self, pos):
        if not self.copyOrCutItemIndexDict:
            self.pasteAction.setEnabled(False)
        else:
            self.pasteAction.setEnabled(True)

        self.blankMainMenu.exec(pos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    assetWindow = ItemWindow()
    assetWindow.show()
    sys.exit(app.exec())
