from PyQt5.QtCore import QFile, QTextStream


def readQss(qssPath):
    file = QFile(qssPath)
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()
