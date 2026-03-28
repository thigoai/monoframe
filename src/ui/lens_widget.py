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
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
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

    def update_frame(self):
        sw = QApplication.primaryScreen().size().width()
        sh = QApplication.primaryScreen().size().height()

        self.setWindowOpacity(0.0)
        QApplication.processEvents()
        time.sleep(0.02)

        raw_img = self.capturer.grab(self.x(), self.y(), self.width(), self.height(), sw, sh)
        self.setWindowOpacity(1.0)

        if raw_img is None:
            return
        
        active_filter_name = self.filter_names[self.current_filter_idx]
        active_filter_func = AVAILABLE_FILTERS[active_filter_name]

        qimg = self.engine.process(raw_img, active_filter_func, self.parameter, self.delay_ms)
        if qimg:
            self.setPixmap(QPixmap.fromImage(qimg))

    def paintEnvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(QColor(0, 255, 0))
        painter.setFont(QFont("Consolas", 10, QFont.bold))

        filer_name = self,self.filter_names[self.current_filter_idx]
        text = f" {filer_name} | {self.parameter:03d} | dly: {self.delay_ms}ms "

        painter.fillRect(5,5,290,20, QColor(0,0,0,160))
        painter.drawText(10, 20, text)
        painter.end()

    def wheelEvent(self, event):
        delta = 5 if event.angleDelta().y() > 0 else -5
        self.intensity = max(0, min(255, self.intensity + delta))

    def keyPressEvent(self, event):
        k = event.key()
        if k in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        elif k == Qt.Key_Up:
            self.delay_ms += 30
        elif k == Qt.Key_Down:
            self.delay_ms = max(0, self.delay_ms - 30)
        elif k == Qt.Key_F: # change the filter
            self.current_filter_idx = (self.current_filter_idx + 1) % len(self.filter_names)
        elif k == Qt.Key_S:
            if self.engine.current_frame is not None:
                agora = datetime.now().strftime('%H%M%S')
                cv2.imwrite(f"img_{agora}.png", self.engine.current_frame)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            diff = event.globalPos() - self.drag_pos
            self.move(self.pos() + diff)
            self.drag_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None