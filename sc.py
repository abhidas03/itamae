import pyautogui
import PIL
import time
x1, y1 = 2024, 974
x2, y2 = 2224, 1074
time.sleep(2)
im = PIL.ImageGrab.grab(bbox=(x1//2, y1//2, x2//2, y2//2))
print(im)
im.save('screenshot2.png')