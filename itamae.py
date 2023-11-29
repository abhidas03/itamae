import pyautogui
import PIL
from PIL import Image, ImageChops, ImageGrab
import time
import numpy as np
import os

IFOLDER = os.listdir('./imgs/zeroed')
BLANK_MAIN = Image.open('./imgs/BLANK_MAIN.png')
FLIP_COLOR = (205, 156, 224)
COORDS = {'main_filling': (2024, 974, 2224, 1074), 'bottom_filling': (2024, 1110, 2224, 1210), 'top_filling': (2024, 840, 2224, 940), 
          'topping': (2024, 672, 2224, 772), 'sauce': (2080, 562, 2517, 620), 'seasoning': (), 'flavor': (1936, 286, 2043, 386), 
          'boba': (2205, 286, 2312, 386), 'flip': (1930, 851, 1950, 871)}

class Order:
    def __init__(self, ricePosition, ingredients, riceTimer=0, flip=False):
        self.ingredients = ingredients
        #stages: cook, build, drinks, tea, serve

        self.currentStage = 'cook'
        self.time = 0
        self.ricePosition = ricePosition
        self.riceTimer = riceTimer
        self.flip = flip

    def update(self, currTime):
        self.time = time

    def getTimeElapsed(self, currTime):
        return currTime - self.time
    
    def getIngredients(self):
        return self.ingredients
    
    def getRicePosition(self):
        return self.ricePosition
    
    def getFlip(self):
        return self.flip
    
    def getCurrentStage(self):
        return self.currentStage
    
    def setCurrentStage(self, stage):
        self.currentStage = stage


#Mac retina display (which i am using) has 2 times the pixels
#If not using mac retina display, comment out the line dividing by 2
#and instead use the line below it
def ret(point):
    return (point.x//2, point.y//2)
    #return (point.x, point.y)

def ret2(coords):
    return (coords[0]//2, coords[1]//2, coords[2]//2, coords[3]//2)

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

#Taken from slowfrog---
def wait_for(f, period=0.5, timeout=30):
    start_time = time.time()
    timeout_elapsed = timeout < 0

    while not (f() or timeout_elapsed):
        time.sleep(period)
        timeout_elapsed = ((time.time() - start_time) > timeout > 0)
    if timeout_elapsed:
        print("Waiting failed: timeout")
        raise Exception("Waiting failed ****** %s" % f)

def lambdifyi(f, params):
    return lambda : f(*params)

#----------------------

def canTakeOrder():
    #TODO: switch to order screen
    n = pyautogui.locateCenterOnScreen('./imgs/order.png', grayscale=True, confidence=0.8)
    return n is not None

def isFlip():
    print('checking if flip')
    flipx = 1940
    flipy = 861
    im = PIL.ImageGrab.grab(bbox=((flipx - 10) // 2, (flipy - 10) // 2, (flipx + 10) // 2, (flipy + 10) // 2)).convert('RGB')
    flipColor = (205, 156, 224)
    flipImageData = list(im.getdata())
    return flipColor in flipImageData

def getFillings():
    fillings = []
    im = ImageGrab.grab(bbox = ret2(COORDS['main_filling'])) 
    im.save('TESTING_RECORD.png')
    im = ImageChops.difference(im, BLANK_MAIN)
    #need to do this for the three filling spots
    #plus every other component of order
    for image in IFOLDER:
        im2 = Image.open('./imgs/zeroed/' + image)
        res = image_err(im, im2)
        if (res < 15):
            print("MATCH FOUND: " + image[:-4], res) 
            fillings.append(image[7:-4])
    return fillings 
    
def getTicket():
    #make ingredients list
    print('starting search')
    ticket = {'fillings': [], 'toppings': [], 'drink': [], 'flip': False}
    ticket['fillings'] = getFillings()
    print(ticket['fillings'])
    ticket['flip'] = isFlip()
    print(ticket['flip'])
    return ticket

def takeOrder():
    #TODO: make sure on order screen before doing this
    n = None
    while n is None:
        n = pyautogui.locateCenterOnScreen('./imgs/order.png', grayscale=True, confidence=0.8)
        time.sleep(0.1)

    pyautogui.click(ret(n))
    # TODO: get ingredients and put everything into game_state,
    time.sleep(5)

    ticket = getTicket()  
    print("order taken", ticket)
    #rice_position = availableRicePot()
    #order = Order(rice_position, ingredients)
    #game_state['orders'].append(order)
    #set order functions
    

def bestAction(game_state):
    #check rice timers (half -> vinegar full -> rice)
    #check orders elapsed time, if > 30s, prioritize
    #do orders

    res = canTakeOrder()
    if res:
        return 'order'
    else:
        return None


def performAction(action, game_state):
    if action == 'order':
        takeOrder()
        '''
        by here, here's what we should have:
        game state has a new order with ingredients list and other info
        order should have been assigned a rice pot, if not, then it will
        have a rice pot value of None and it needs to be dealt with as soon as one opens

        next up is to perform the next best action, which will probably be to go to 
        building the orders, or adding vinegar to an order, or removing rice from pot 
        '''
    else:
        print('no action')

def startGame():
    print('starting game...')
    n = pyautogui.locateCenterOnScreen('./imgs/play.png', grayscale=True, confidence=0.8)
    if n == None:
        print("didn't find play button, continuing as if game is already started")
        return
    pyautogui.click(ret(n))
    time.sleep(1.25)
    n = None
    while n is None:
        n = pyautogui.locateCenterOnScreen('./imgs/select.png', grayscale=True, confidence=0.8)
        time.sleep(0.1)
    pyautogui.click(ret(n))

'''
Initializes game state
Performs start sequence if needed
(starts cooking rice)
waits for first order
enters main game loop:
    - finds next best action
        :check rice timers for vinegar and make sure don't overcook
        :need to check for any blockers (if rice can't move on, will overcook orders)
        :if there is a rice pot open, take order
        :otherwise, build orders (if no food left, then do drinks)
    - performs action
'''
def play():
    time.sleep(2)

    game_state = {
                  'orders': [], 
                  'rice_timer': [], 
                  'running': True,
                  'rice_pots': [0, 0, 0]
                 }
    startGame()
    lamb = lambdifyi(canTakeOrder, [])
    print('waiting for orders...')

    wait_for(lamb, period=0.2, timeout=30)
    while (game_state['running']):
        action = bestAction(game_state)
        performAction(action, game_state)
        #update game_state time elapsed on each order
        
        time.sleep(1)


play()
