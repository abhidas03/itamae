import PIL
from PIL import Image, ImageGrab
import time

#MAIN INGREDIENT
x1, y1 = 2024, 974
x2, y2 = 2224, 1074

#BOTTOM INGREDIENT
# x1, y1 = 2024, 1110
# x2, y2 = 2224, 1215

time.sleep(2)
GROUND = "BLANK"
im = PIL.ImageGrab.grab(bbox=(x1//2, y1//2, x2//2, y2//2))
im.save("./imgs/ingredients/" + GROUND + ".png")