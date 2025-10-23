import cv2
from .vision import count_jellyfish_snapshot

class JellyStream:
    def __init__(self, url: str):
        self.url = url
        self.cap = None

    def open(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)

    def snapshot_count(self) -> int:
        if self.cap is None or not self.cap.isOpened():
            self.open()
        return count_jellyfish_snapshot(self.cap)

    def close(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
