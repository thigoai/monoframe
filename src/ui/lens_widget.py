import cv2
from datetime import datetime
from enum import Enum, auto

from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

from core.capturer import ScreenCapturer
from core.vision_engine import VisionEngine
from core.filters import AVAILABLE_FILTERS

class AppState(Enum):
    RUNNING = auto()
    PAUSED = auto()

class HUDWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("""
            QLabel {
                color: #E0E0E0; 
                background-color: rgba(20, 20, 20, 180);
                border: 1px solid rgba(255, 255, 255, 50);
                border-radius: 6px;
                padding: 4px 10px;
                font-family: 'Consolas', monospace;
                font-weight: bold;
                font-size: 11px;
            }
        """)

    

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

        self.hud = HUDWidget()
        self.hud.show()

        self.state = AppState.RUNNING

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(60) 

    def update_frame(self):
        if self.state == AppState.PAUSED:
            return

        if self.state == AppState.RUNNING:
            self.setWindowOpacity(0.0)
            QTimer.singleShot(10, self._perform_capture)

    def _perform_capture(self):
        if self.state != AppState.RUNNING:
            return

        sw = QApplication.primaryScreen().size().width()
        sh = QApplication.primaryScreen().size().height()
        raw_img = self.capturer.grab(self.x(), self.y(), self.width(), self.height(), sw, sh)

        self.setWindowOpacity(1.0)

        if raw_img is not None:
            active_filter_name = self.filter_names[self.current_filter_idx]
            active_filter_func = AVAILABLE_FILTERS[active_filter_name]

            qimg = self.engine.process(raw_img, active_filter_func, self.parameter, self.delay_ms)
            if qimg:
                self.setPixmap(QPixmap.fromImage(qimg))
                
            self.hud.setText(f" * {active_filter_name} | {self.parameter:03d} ")

    def wheelEvent(self, event):
        delta = 5 if event.angleDelta().y() > 0 else -5
        self.parameter = max(0, min(255, self.parameter + delta))

    def keyPressEvent(self, event):
        k = event.key()
        if k in (Qt.Key_Escape, Qt.Key_Q):
            self.close()
        elif k == Qt.Key_Space: 
            if self.state == AppState.PAUSED:
                self.state = AppState.RUNNING
            else:
                self.state = AppState.PAUSED
        elif k == Qt.Key_Up:
            self.delay_ms += 30
        elif k == Qt.Key_Down:
            self.delay_ms = max(0, self.delay_ms - 30)
        elif k == Qt.Key_F: 
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

    def moveEvent(self, event):
        super().moveEvent(event)
        self._update_hud_position()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_hud_position()
        
    def _update_hud_position(self):
        hud_x = self.x()
        hud_y = self.y() - 30 
        
        if hud_y < 0:
            hud_y = self.y() + self.height() + 5
            
        self.hud.move(hud_x, hud_y)
        self.hud.resize(self.width(), 25)

    def closeEvent(self, event):
        self.hud.close()
        super().closeEvent(event)