from PySide.QtCore import QObject, Signal
from Queue import Queue
import json, os, urllib2
import tmdbsimple as tmdb
from threading import Thread


tmdb.API_KEY = '83cbec0139273280b9a3f8ebc9e35ca9'
posterPathString = "https://image.tmdb.org/t/p/w300/"
backdropPathString = "https://image.tmdb.org/t/p/w500/"

dataFolder = os.path.expanduser('~/Documents/MovieLibrary/')

class GetInfo(QObject):
    downloadFinished = Signal()

    def __init__(self):
        super(GetInfo, self).__init__()

        self.movieQueue = Queue()
        self.progress = True
        self.currentDownload = None

    def setMovies(self, movieObjects):
        for obj in movieObjects:
            self.movieQueue.put(obj)

        self.getData()

    def getData(self):
        # start downloadig progress
        t = Thread(target=getInfoWorker, args=(self.movieQueue, self.downloadFinished))
        t.start()


def getInfoWorker(queue, signal):

    while not queue.empty():
        movieObj = queue.get()

        movieData = getMovieData(movieObj.name)
        movieObj.setData(movieData)

        # process ready
        queue.task_done()
        signal.emit()


def getMovieData(movieTitle):
    if not os.path.exists(dataFolder):
        os.mkdir(dataFolder)

    # get data from file if exists
    if os.path.exists(dataFolder + movieTitle + "_data_.json"):
        with open(dataFolder + movieTitle + "_data_.json") as configFile:
            return json.load(configFile)


    search = tmdb.Search()
    search.movie(query=movieTitle)

    print "downloading movie data:", movieTitle

    result = search.results
    if result:
        dataDict = result[0]
        if dataDict["poster_path"]:
            dataDict["poster_path"] = posterPathString + dataDict["poster_path"]

            # save poster
            posterFile = downloadImage(dataDict["poster_path"], movieTitle + "_poster_")
            dataDict["posterFile"] = posterFile


        if dataDict["backdrop_path"]:
            dataDict["backdrop_path"] = backdropPathString + dataDict["backdrop_path"]

            # download backdrop image
            backdropFile = downloadImage(dataDict["backdrop_path"], movieTitle + "_backdrop_")

            dataDict["backdropFile"] = backdropFile


        # save data
        saveData(dataDict, movieTitle)

        return dataDict

    return {}

def saveData(data, title):
    print "saving data for", title

    with open(dataFolder + title + "_data_.json", "w") as dataFile:
        json.dump(data, dataFile)

def downloadImage(imageLink, title):
    print "downloading image for", title

    imageFile = open(dataFolder + title + ".jpg", "wb")
    imageFile.write(urllib2.urlopen(imageLink).read())
    imageFile.close()

    return dataFolder + title + ".jpg"

if __name__ == "__main__":
    getMovieData("Star Wars")