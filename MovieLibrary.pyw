from PySide.QtGui import QApplication, QMainWindow, QIcon, QHBoxLayout, \
    QWidget, QSplitter
from PySide.QtCore import Qt, QSettings
import sys, os

# get window icon on taskbar
import ctypes
myappid = 'RovaSoft.MovieLibrary' # arbitrary string
#ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from utils import fileUtils
from modules import folderBrowser, movieDetails, posterView

class MovieLibraryWindow(QMainWindow):
    def __init__(self):
        super(MovieLibraryWindow, self).__init__()
        self.setWindowTitle("Movie Library")
        self.setWindowIcon(QIcon(fileUtils.getIcon("windowIcon.png")))

        self.settings = QSettings("RoVa Soft", "Movie Library")

        if self.settings.value("geometry"):
            self.restoreGeometry(self.settings.value("geometry"))

        # add central widget and mainLayout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout(centralWidget)

        splitter = QSplitter(Qt.Horizontal)
        mainLayout.addWidget(splitter)

        # load modules
        self.folderBrowser = folderBrowser.FolderBrowser(self)
        self.posterView = posterView.PosterView(self)

        self.folderBrowser.folderChanged.connect(self.posterView.folderChangedAction)

        # TODO show when poster double clicked
        self.movieDetails = movieDetails.MovieDetails(self)
        self.movieDetails.setVisible(False)

        splitter.addWidget(self.folderBrowser)
        splitter.addWidget(self.posterView)
        splitter.setSizes([200, 1000])

        self.applyStyle()

    def applyStyle(self):
        with open(fileUtils.getIcon("style.qss")) as dataFile:
            style = dataFile.read()
            self.setStyleSheet(style)

    def closeEvent(self, *args, **kwargs):
        self.settings.setValue("geometry", self.saveGeometry())


app = QApplication(sys.argv)
win = MovieLibraryWindow()
win.show()
app.exec_()