import PIL
from PIL import Image, ImageGrab
import numpy 
import time
import pyautogui
#MAIN INGREDIENT
coords = {'main': [(2024, 974, 2224, 1074)]}
x1, y1 = 2024, 974
x2, y2 = 2224, 1074

#BOTTOM INGREDIENT
# x1, y1 = 2024, 1110
# x2, y2 = 2224, 1210

#TOP INGREDIENT
x1, y1 = 2024, 840
x2, y2 = 2224, 940
time.sleep(2)
GROUND = "BLANK"
#im = PIL.ImageGrab.grab(bbox=(x1//2, y1//2, x2//2, y2//2))
#im.save("./imgs/ingredients/" + GROUND + ".png")
flipx = 1940
flipy = 861
im = PIL.ImageGrab.grab(bbox=((flipx - 10) // 2, (flipy - 10) // 2, (flipx + 10) // 2, (flipy + 10) // 2)).convert('RGB')
flipImageData = list(im.getdata())
flipColor = (205, 156, 224)
if flipColor in flipImageData:
    print("FLIP")
else:
    print("NO")
#im.save("flip.png")
