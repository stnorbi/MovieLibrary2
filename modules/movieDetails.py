from PySide.QtGui import QWidget

class MovieDetails(QWidget):
    def __init__(self, mainWindow):
        super(MovieDetails, self).__init__()
        self.mainWindow = mainWindow