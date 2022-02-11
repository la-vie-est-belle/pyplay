from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SceneWindowBase(QGraphicsView):
    def __init__(self):
        super(SceneWindowBase, self).__init__()
        # self.setAttribute(Qt.WA_TranslucentBackround)

    """Events"""
    def wheelEvent(self, event):
        ...