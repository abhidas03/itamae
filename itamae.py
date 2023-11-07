import pyautogui
import PIL.ImageGrab as yoink
import time
import numpy as np
import random

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
    #switch to order screen
    n = pyautogui.locateCenterOnScreen('./imgs/order.png', grayscale=True, confidence=0.8)
    if n is None:
        return False
    else:
        return True

def recordIngredients():
    #make ingredients list
    ingredients = set()
    boxList = [(1012, 487, 1112, 537)]
    i = 0
    for bbox in boxList:
        yoink(bbox).save('ingredient{i}.png')
        i += 1
    ingredients.add('rice')
    flip = False
    return ingredients, flip

def takeOrder():
    #TODO: make sure on order screen before doing this
    n = None
    while n is None:
        n = pyautogui.locateCenterOnScreen('./imgs/order.png', grayscale=True, confidence=0.8)
        time.sleep(0.1)

    pyautogui.click(ret(n))
    # TODO: get ingredients and put everything into game_state,

    ingredients = recordIngredients()  
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

def play():
    time.sleep(2)

    game_state = {
                  'orders': {}, 
                  'rice_timer': [], 
                  'running': True,
                  'rice_pots': [0, 0, 0]
                 }
    startGame()
    lamb = lambdifyi(canTakeOrder, [])
    print('waiting for orders...')

    wait_for(lamb, period=0.5, timeout=30)
    while (game_state['running']):
        action = bestAction(game_state)
        performAction(action, game_state)
        #update game_state time elapsed on each order
        time.sleep(1)


play()
