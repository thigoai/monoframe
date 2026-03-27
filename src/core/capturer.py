import mss
import numpy as np

class ScreenCapturer:
    def __init__(self):
        self.sct = mss.mss()

    def grab(self, x, y, w, h, screen_w, screen_h):

        x, y = max(0, x), max (0, y)

        w = min(w, screen_w - x)
        h = min(h, screen_h -y)

        if w <= 0 or h <= 0:
            return None
        
        monitor = {
            "top": int(y), 
            "left": int(x), 
            "width": int(w), 
            "height": int(h)
            }
        try:
            return np.array(self.sct.grab(monitor))
        except Exception:
            return None
