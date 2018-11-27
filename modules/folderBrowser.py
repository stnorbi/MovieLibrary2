from PySide.QtGui import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, \
    QLabel, QHBoxLayout, QPushButton, QFileDialog, QIcon
from PySide.QtCore import Qt, Signal

import customWidgets
from utils import fileUtils

class FolderBrowser(QWidget):
    folderChanged = Signal(list)

    def __init__(self, mainWindow):
        super(FolderBrowser, self).__init__()
        self.mainWindow = mainWindow

        self.config = fileUtils.loadConfig()
        self.movieFiles = []

        mainlayout = QVBoxLayout(self)
        mainlayout.setContentsMargins(0,0,0,0)

        buttonlayout = QHBoxLayout()
        buttonlayout.setAlignment(Qt.AlignLeft)
        buttonlayout.setContentsMargins(0,0,0,0)

        mainlayout.addLayout(buttonlayout)

        addFolderBtn = customWidgets.IconButton(fileUtils.getIcon("addFolder.png"), "Add Folder", size=40)
        removeFolderBtn = customWidgets.IconButton(fileUtils.getIcon("removeFolder.png"), "Remove Folder", size=40)

        addFolderBtn.clicked.connect(self.addFolderAction)
        removeFolderBtn.clicked.connect(self.removeFolderAction)

        buttonlayout.addWidget(addFolderBtn)
        buttonlayout.addWidget(removeFolderBtn)

        self.folderList = FolderList(self)
        if "folders" in self.config:
            self.folderList.refresh()

        mainlayout.addWidget(self.folderList)

        self.folderList.itemClicked.connect(self.getFiles)

    def getFiles(self, *args):
        currentItem = args[0]
        self.movieFiles = fileUtils.getMovieFiles(currentItem.folderPath)

        self.folderChanged.emit(self.movieFiles)

    def addFolderAction(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Add Folder", "/")

        if len(folderPath):
            if "folders" in self.config:
                self.config["folders"].append(folderPath)
            else:
                self.config["folders"] = [folderPath]

            fileUtils.saveConfig(self.config)

            # refresh folder list
            self.folderList.refresh()

    def removeFolderAction(self):
        currentItem = self.folderList.currentItem()
        if not currentItem: return

        folderText = currentItem.folderPath
        self.config["folders"].remove(folderText)

        fileUtils.saveConfig(self.config)

        self.folderList.refresh()

class FolderList(QListWidget):
    def __init__(self, parent):
        super(FolderList, self).__init__(parent)

    def refresh(self):
        self.clear()

        for folder in self.parent().config["folders"]:
            folderItem = FolderItem(folder, self)


class FolderItem(QListWidgetItem):
    def __init__(self, folderPath, parent):
        super(FolderItem, self).__init__(parent)
        self.setText(folderPath.split("\\")[-1])

        self.folderPath = folderPath
        self.setIcon(QIcon(fileUtils.getIcon("addFolder.png")))