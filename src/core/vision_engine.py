from collections import deque
from PyQt5.QtGui import QImage

class VisionEngine:
    def __init__(self):
        self.frame_buffer = deque(maxlen=1)
        self.current_frame = None
