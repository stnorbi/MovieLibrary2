from PySide.QtGui import QDialog, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout
from utils import dataDownloader
from classes import Movie

class EditMovieWindow(QDialog):
    def __init__(self,parent):
        super(EditMovieWindow,self).__init__(parent)
        self.setModal(True)
        self.resize(500,500)
        #self.setWindowTitle("Edit Movie: {}".format(movieObject.name))

        self.movieObject=None

        mainLayout=QVBoxLayout(self)

        getMoviesBtn=QPushButton("Get movies from Movie DB")

        self.resultListView=QListWidget()
        self.resultListView.itemDoubleClicked.connect(self.editData)

        mainLayout.addWidget(getMoviesBtn)
        mainLayout.addWidget(self.resultListView)

        getMoviesBtn.clicked.connect(self.getMoviesAction)

    def getMoviesAction(self):
        movieList=dataDownloader.movieDBSearch(self.movieObject.name)

        for movie in movieList:
            movieItem=MovieItem(movie, self.restultListView)

    def editData(self):
        selectedItem=self.resultListView.currentItem()

        data=selectedItem.movieData

         # todo download new poster
        if data["poster_path"]:
            dataDownloader.downloadImage(data["poster_path"],self.movieObject.name)

        # todo download backdrop image
        if data["backdrop_path"]:
            dataDownloader.downloadImage(data["backdrop_path"], self.movieObject.name)


        # todo edit data in database
        self.movieObject.editData(data)

        self.accept()


    def setMovie(self,movieObject):
        self.setWindowTitle("Edit Movie: {}".format(movieObject.name))
        self.movieObject

class MovieListView(QListWidget):
    def __init__(self,data,parent):
        super(MovieListView,self).__init__(parent)
        self.movieData=data

        #self.setText(data[])

class MovieItem(QListWidget):
    def __init__(self):
        super(MovieListView,self).__init__(parent)
        self.movieData=data


if __name__=="__main__":
    from PySide.QtGui import QDialog, QApplication
    import sys
    from classes import Movie
    testMovie=Movie.Movie("/media/norbert/Datas/Filmek/Tomb.Raider.2018.BDRiP.x264.HuN-Gold/TombRaider.mkv")

    app=QApplication(sys.argv)
    win=EditMovieWindow(None)
    win.show()
    app.exec_()



