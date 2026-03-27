from collections import deque
from PyQt5.QtGui import QImage

class VisionEngine:
    def __init__(self):
        self.frame_buffer = deque(maxlen=1)
        self.current_frame = None

    def process(self, raw_img, filter_func, parameter, delay_ms):
        if raw_img is None:
            return None
        
        processed = filter_func(raw_img, parameter)

        required_frames = max(1, int(delay_ms / 30))

        self.frame_buffer.append(processed)
        frame = self.frame_buffer[0]

        fh, fw = frame.shape
        self.current_frame = frame.copy()

        return QImage(self.current_frame.data, fw, fh, fw, QImage.Format_Grayscale8)