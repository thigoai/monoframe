import mss
import numpy as np

class ScreenCapturer:
    def __init__(self):
        self.sct = mss.mss()
