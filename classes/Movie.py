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
        self.favorited=True

    def getData(self):
        self.data=DB_API.getData(self.path)
        self.poster=self.data["posterFile"]
        self.backdrop=self.data["backdropFile"]


        # dataFile= dataDownloader.dataFolder + self.name + "_data_.json"
        # data=None
        #
        # if os.path.exists(dataFile):
        #     with open(dataFile) as configFile:
        #         data= json.load(configFile)
        #
        #     self.data=data
        #     self.releaseDate=int(data["release_date"].split("-")[0])
        #
        #     if "posterFile" in self.data:
        #         self.poster=self.data["posterFile"]
        #
        #     if "backdropFile" in self.data:
        #         self.backdrop = self.data["backdropFile"]


    def saveData(self,dataDict):
        dataDict["path"]=self.path
        self.poster=dataDict["posterFile"]
        self.backdrop=dataDict["backdropFile"]

        # save data to mongoDb
        self._id=DB_API.insertData(dataDict)



    def play(self):
        pass

    def copy(self):
        pass

    def delete(self):
        pass