import os, json
from utils import dataDownloader
from utils import fileUtils, DB_API


dataFolder = os.path.expanduser('~/Documents/MovieLibrary/')

class Movie():
    def __init__(self, filePath):
        self._id = None
        self.dbCollection="movies"

        self.path = filePath

        filename, ext = os.path.splitext(filePath)
        self.name = os.path.basename(filePath).replace(ext, "")

        self.data = {}
        self.releaseDate = None
        self.poster = fileUtils.getIcon("collectingData.png")
        self.backdrop=None
        #self.poster = r"/media/norbert/Datas/Python/Python_Suli_Master/Master_02/megoldas/iconsAliens.jpg"
        self.favorited=False


    def setFavorited(self):
        self.favorited=not self.favorited
        data=self.data

        data["favorited"]=self.favorited

        self.saveData(self.data)
        self.editData(self.data)


    def getData(self):
        result=DB_API.getData(self.path)

        if result:
            self.data=result
            self._id=result["_id"]
            self.poster=self.data["posterFile"]
            self.backdrop=self.data["backdropFile"]
            self.releaseDate=result["release_date"]


    def saveData(self,dataDict):
        dataDict["path"]=self.path
        self.poster=dataDict["posterFile"]
        self.backdrop=dataDict["backdropFile"]

        # save data to mongoDb
        self._id=DB_API.insertData(dataDict)


    def editData(self, dataDict):
        dataDict["_id"]=self._id
        DB_API.editData(dataDict)




    def play(self):
        pass

    def copy(self):
        pass

    def delete(self):
        # # delete movie file
        # os.remove(self.path)
        #
        # # delete image files
        # os.remove(self.poster)
        # os.remove(self.backdrop)

        # delete database entry
        DB_API.deleteData(self._id)
