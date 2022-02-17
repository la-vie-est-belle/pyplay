import uuid
import time
import json
from pathlib import Path
from PyQt5.QtCore import QFile, QTextStream, Qt


def getQssPath(qssName):
    return str(Path(__file__).parent / 'res' / 'qss' / qssName)


def getImagePath(imgName):
    return str(Path(__file__).parent / 'res' / 'image' / imgName)


def getUUID():
    UUID = uuid.uuid3(uuid.NAMESPACE_OID, str(time.time()))
    return str(UUID)


def readQss(qssName):
    file = QFile(getQssPath(qssName))
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()


def updateItemStructureFile(structureDict, model):
    structureDict.clear()

    for row in range(model.rowCount()):
        item = model.item(row, 0)
        getStructureRecursively(structureDict, item)

    with open('itemStructure.json', 'w') as f:
        f.write(json.dumps(structureDict))


def getStructureRecursively(structureDict, parentItem):
    structureDict[parentItem.UUID] = []

    if parentItem.hasChildren():
        for i in range(500):
            childItem = parentItem.child(i, 0)
            if childItem:
                childUUID = parentItem.child(i, 0).UUID
                structureDict[parentItem.UUID].append(childUUID)
                getStructureRecursively(structureDict, childItem)
            else:
                break


def setItemAlignment(item, alignment):
    if alignment == 1:
        item.setAlignment(Qt.AlignLeft)
    elif alignment == 2:
        item.setAlignment(Qt.AlignRight)
    elif alignment == 4:
        item.setAlignment(Qt.AlignHCenter)
    elif alignment == 32:
        item.setAlignment(Qt.AlignTop)
    elif alignment == 64:
        item.setAlignment(Qt.AlignBottom)
    elif alignment == 128:
        item.setAlignment(Qt.AlignVCenter)
    elif alignment == 33:
        item.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    elif alignment == 65:
        item.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
    elif alignment == 129:
        item.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    elif alignment == 34:
        item.setAlignment(Qt.AlignRight | Qt.AlignTop)
    elif alignment == 66:
        item.setAlignment(Qt.AlignRight | Qt.AlignBottom)
    elif alignment == 130:
        item.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
    elif alignment == 36:
        item.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
    elif alignment == 68:
        item.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
    elif alignment == 132:
        item.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
