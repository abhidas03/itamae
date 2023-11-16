import pyautogui
import PIL
from PIL import Image, ImageChops
import numpy as np
import os


import time
iFolder = os.listdir('./imgs/zeroed')

#get list of ingredients
# ingredientsList = []
# for ingredient in iFolder:
#     ingredientsList.append(ingredient[:-4])

#msre image error
def image_err(image1, image2):
    image1 = image1.convert('L')
    image2 = image2.convert('L')
    diff = ImageChops.difference(image1, image2)
    imageData = list(diff.getdata())
    imageData = np.array(imageData)
    h, w = diff.size
    err = np.sum(imageData ** 2)
    mse = err/(float(h*w))
    return mse**0.5

#MAIN INGREDIENT
x1, y1 = 2024, 974
x2, y2 = 2224, 1074

#BOTTOM INGREDIENT
# x1, y1 = 2024, 1110
# x2, y2 = 2224, 1215

time.sleep(2)
GROUND = 'edamame'
im = PIL.ImageGrab.grab(bbox=(x1//2, y1//2, x2//2, y2//2))
blank = Image.open('imgs/BLANK.png')
im = ImageChops.difference(im, blank)

# im2 = Image.open(f'./imgs/zeroed/ZEROED_{GROUND}.png')


# res = image_err(im, im2)
# print(res)

for image in iFolder:
    im2 = Image.open('./imgs/zeroed/' + image)
    res = image_err(im, im2)
    if (res < 25):
        print("MATCH FOUND: " + image[:-4], GROUND, res) 