import time
import cv2
import numpy as np
from . import config
from .utils import log

def compute_mask(frame_bgr, hsv_low, hsv_high, open_iters, close_iters):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    mask_blue = cv2.inRange(hsv, hsv_low, hsv_high)  # 255 where blue
    keep_mask = cv2.bitwise_not(mask_blue)           # 255 where NOT blue
    kernel = np.ones((3, 3), np.uint8)
    if open_iters > 0:
        keep_mask = cv2.morphologyEx(keep_mask, cv2.MORPH_OPEN, kernel, iterations=open_iters)
    if close_iters > 0:
        keep_mask = cv2.morphologyEx(keep_mask, cv2.MORPH_CLOSE, kernel, iterations=close_iters)
    return keep_mask

def count_jellyfish_snapshot(cap) -> int:
    log("Counting jellyfish…")
    best = 0
    tries = 0
    while tries < config.COUNT_GRACE_FRAMES:
        ok, frame = cap.read()
        if not ok or frame is None:
            time.sleep(0.2)
            tries += 1
            continue
        mask = compute_mask(
            frame,
            np.array(config.MASK_LOWER, dtype=np.uint8),
            np.array(config.MASK_UPPER, dtype=np.uint8),
            config.OPEN_ITERS,
            config.CLOSE_ITERS,
        )
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rects = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) >= config.MIN_AREA]
        best = max(best, len(rects))
        tries += 1
        time.sleep(0.05)
    return best
