from PySide.QtGui import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, \
    QLabel, QItemDelegate, QBrush, QPen, QColor, QPixmap, QStyle, QMessageBox, QHBoxLayout, QPushButton
from PySide.QtCore import QSize, Qt, QRect
from utils import dataDownloader
import EditMovieDialog

from classes.Movie import Movie

class PosterView(QWidget):
    def __init__(self, mainWindow):
        super(PosterView, self).__init__()
        self.mainWindow = mainWindow

        mainlayout = QVBoxLayout(self)
        mainlayout.setContentsMargins(0, 0, 0, 0)

        toolbarLayout=QHBoxLayout()
        toolbarLayout.setAlignment(Qt.AlignLeft)
        mainlayout.addLayout(toolbarLayout)

        favBtn=QPushButton("Fav")
        favBtn.setMaximumWidth(50)
        editBtn=QPushButton("Edit")
        editBtn.setMaximumWidth(50)

        toolbarLayout.addWidget(favBtn)
        toolbarLayout.addWidget(editBtn)

        self.posterList = PosterList()
        mainlayout.addWidget(self.posterList)



        favBtn.clicked.connect(self.posterList.setFavorited)
        editBtn.clicked.connect(self.posterList.editMovie)

    def folderChangedAction(self, *args):
        self.posterList.refresh(args[0])



class PosterList(QListWidget):
    def __init__(self):
        super(PosterList, self).__init__()
        self.setItemDelegate(PosterViewDelegate())

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setSpacing(10)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setMovement(QListWidget.Static)

        self.GetInfo=dataDownloader.GetInfo()
        self.GetInfo.downloadFinished.connect(self.repaint)

        self.editMovieDialog=EditMovieDialog.EditMovieWindow(self)

    def setFavorited(self):
        selectedMovie=self.currentItem()

        if not selectedMovie: return

        selectedMovie.movieObject.setFavorited()

    def editMovie(self):
        selectedMovie=self.currentItem()
        if not selectedMovie: return

        self.editMovieDialog.setMovie(selectedMovie.movieObject)
        self.editMovieDialog.show()


    def keyPressEvent(self,event):
        selectedMovie=self.currentItem()
        if not selectedMovie: return

        if event.key()==Qt.Key_Delete:
            movieObject=selectedMovie.movieObject

            msg=QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Do you Want to delete {}?".format(movieObject.name))
            msg.setWindowTitle("Delete Movie")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.show()

            if msg.exec_()==QMessageBox.Ok:
                selectedMovie.movieObject.delete()

                self.takeItem(self.row(selectedMovie))


    def refresh(self, movieList):
        self.clear()

        downloadDataList=[]
        movieObjects=[]

        for file in movieList:
            movie = Movie(file)
            movieObjects.append(movie)

            if not movie.data:
                downloadDataList.append(movie)

        for m in sorted(movieObjects,key=lambda movieObject: movieObject.releaseDate, reverse=True):
            posterItem = PosterItem(m, self)

        if downloadDataList:
            self.GetInfo.setMovies(downloadDataList)



class PosterItem(QListWidgetItem):
    def __init__(self, movieObject, parent):
        super(PosterItem, self).__init__(parent)
        self.movieObject=movieObject

        self.setSizeHint(QSize(320, 490))
        self.setData(Qt.UserRole, movieObject)


class PosterViewDelegate(QItemDelegate):
    def __init__(self):
        super(PosterViewDelegate, self).__init__()

        self.backgoundBrush = QBrush(QColor("#111"))
        self.selectedBrush = QBrush(QColor(255,255,255,50))
        self.outline = QPen(QColor("#999"))

    def paint(self, painter, option, index):
        rect = option.rect
        movie = index.data(Qt.UserRole)

        painter.setOpacity(0.7)
        if option.state & QStyle.State_Selected:
            painter.drawRect(rect)


        # draw poster background
        painter.setPen(self.outline)
        painter.setBrush(self.backgoundBrush)
        painter.drawRect(rect)

        # draw poster
        pixmap = QPixmap(movie.poster).scaled(rect.width()-25, rect.height()-50, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        posterRect = QRect(rect.x() + 15, rect.y() + 15, pixmap.width(), pixmap.height())
        painter.drawPixmap(posterRect, pixmap)

        # draw movie title
        titleRect = QRect(rect.x(), rect.bottom()-30, rect.width(), rect.height())

        releaseText="({})".format(movie.releaseDate.split("-")[0]) if movie.releaseDate else ""
        painter.drawText(titleRect, Qt.AlignHCenter, u"{0} {1}".format(movie.name, releaseText))

        # draw favicon
        # if movie.favorited:
        #     faviconRect=QRect(rect.x()+5,rect()+5,30,30)
