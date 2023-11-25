import pyautogui
import PIL
from PIL import Image, ImageChops
import numpy as np
import os


import time
iFolder = os.listdir('./imgs/zeroed/')

for image in iFolder:
    im1 = Image.open(f'./imgs/ingredients/{image}')
    im2 = Image.open('blank.png')
    im1 = im1.convert('L')
    im2 = im2.convert('L')
    diff = ImageChops.difference(im1, im2)
    diff.save('./imgs/zeroed/ZEROED_' + image)
