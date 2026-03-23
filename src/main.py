from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor
import sys

class JanelaTransparente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |  
            Qt.WindowStaysOnTopHint    
        )
        self.setAttribute(Qt.WA_TranslucentBackground) 
        self.resize(700, 500)
        self._drag_pos = QPoint()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

    def mousePressEvent(self, e):
        self._drag_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = e.globalPos() - self._drag_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self._drag_pos = e.globalPos()

    def paintEvent(self, e):
        from PyQt5.QtGui import QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0, 120)) 
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

app = QApplication(sys.argv)
win = JanelaTransparente()
win.show()
sys.exit(app.exec_())