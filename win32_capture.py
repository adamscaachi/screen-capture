import time
import numpy as np
import win32gui, win32ui, win32con

class Capture:
    def __init__(self, x, y, width, height):
        self.hwnd = win32gui.GetDesktopWindow()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hwindc = win32gui.GetWindowDC(self.hwnd)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.srcdc, width, height)
        self.memdc.SelectObject(self.bitmap)

    def get_capture(self):
        self.memdc.BitBlt((0, 0), (self.width, self.height), self.srcdc, (self.x, self.y), win32con.SRCCOPY)
        bitmap_bits = self.bitmap.GetBitmapBits(True)
        capture = np.frombuffer(bitmap_bits, dtype='uint8')
        capture.shape = (self.height, self.width, 4)       
        capture = capture[..., 0]  # BGRA to B
        return capture

    def cleanup(self):
        self.srcdc.DeleteDC()
        self.memdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwindc)
        win32gui.DeleteObject(self.bitmap.GetHandle())

if __name__ == "__main__":
    width = 2880
    height = 1800
    num_samples = 1000
    capture = Capture(0, 0, width, height)
    start_time = time.time()
    for _ in range(num_samples):
        capture.get_capture()
    frame_duration = 1000.0 * (time.time() - start_time) / num_samples
    print(f"{width}x{height} - {frame_duration:.2f} ms")