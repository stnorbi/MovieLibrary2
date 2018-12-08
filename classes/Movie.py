import os
from utils import DB
from utils import fileUtils

class Movie():
    def __init__(self, filePath):
        self._id = None

        self.path = filePath

        filename, ext = os.path.splitext(filePath)
        self.name = os.path.basename(filePath).replace(ext, "")

        self.data = {}
        self.releaseDate = "1986"
        self.poster = fileUtils.getIcon("collectingData.png")
        self.backdrop=None
        #self.poster = r"/media/norbert/Datas/Python/Python_Suli_Master/Master_02/megoldas/iconsAliens.jpg"
        self.favorited=True

    def getData(self):
        data=DB.getMovieData(self.name)

        if data:
            self.data=data
            if "posterFile" in self.data:
                self.poster=self.data["posterFile"]

            if "backdropFile" in self.data:
                self.backdrop = self.data["backdropFile"]

    def setMovie(self,dataDict):
        self.data=dataDict

        if data:
            self.data=data
            if "posterFile" in self.data:
                self.poster=self.data["posterFile"]

            if "backdropFile" in self.data:
                self.backdrop = self.data["backdropFile"]

    def setData(self, dataDict):
        self.data = dataDict

        if "posterFile" in self.data:
            self.poster = self.data["posterFile"]

        if "backdropFile" in self.data:
            self.backdrop = self.data["backdropFile"]

    def play(self):
        pass

    def copy(self):
        pass

    def delete(self):
        pass