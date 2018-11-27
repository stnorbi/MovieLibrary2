from PySide.QtGui import QWidget, QPainter, QPixmap, QApplication
from PySide.QtCore import Qt, Signal

class IconButton(QWidget):
    clicked = Signal()
    def __init__(self, icon, tooltip, size=30):
        super(IconButton, self).__init__()
        self.setMaximumSize(size, size)
        self.setMinimumSize(size, size)

        self.highlighted = False

        self.icon = QPixmap(icon)
        self.setToolTip(tooltip)

    def mousePressEvent(self, *args, **kwargs):
        self.clicked.emit()

    def enterEvent(self, *args, **kwargs):
        self.highlighted = True
        QApplication.setOverrideCursor(Qt.PointingHandCursor)
        self.repaint()

    def leaveEvent(self, *args, **kwargs):
        self.highlighted = False
        QApplication.restoreOverrideCursor()
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw(painter)
        painter.end()

    def draw(self, painter):
        rect = self.rect()

        painter.setOpacity(0.5)
        if self.highlighted:
            painter.setOpacity(1.0)

        painter.drawPixmap(rect, self.icon)