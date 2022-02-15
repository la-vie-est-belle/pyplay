import uuid
import time
import json
from pathlib import Path
from PyQt5.QtCore import QFile, QTextStream


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