from PyQt5.QtGui import *

from util import getUUID


class BasicTreeViewItem(QStandardItem):
    def __init__(self, itemName, UUID=None):
        super(BasicTreeViewItem, self).__init__(itemName)
        self.UUID = UUID if UUID else getUUID()