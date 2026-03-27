import time
import cv2
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont

from core.capturer import ScreenCapturer
from core.vision_engine import VisionEngine
from core.filters import AVAILABLE_FILTERS

class FilterLens(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(350, 200)

        self.parameter = 127
        self.delay_ms = 0
        self.drag_pos = None

        self.filter_names = list(AVAILABLE_FILTERS.keys())
        self.current_filter_idx = 0

        self.capturer = ScreenCapturer()
        self.engine = VisionEngine()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)