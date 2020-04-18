###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: colorMovingObject.py
###############################################################################
'''
    Just overlapping code from pandas3DTest.py and colorTracker.py.
    I tried to ram all the code into one file, which didnt work.
    See files listed above for citations.
    -
'''



from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from panda3d.physics import *

#for basic intervals
from direct.interval.IntervalGlobal import *
from direct.interval.LerpInterval import *

import sys, math, os, random

#for task managers
from direct.task.Task import Task
import time
import cv2
import numpy as np
import threading

class TermProject(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModels()
        #self.cappture()
        #self.circularMovement(self.shape)
        #self.circularMovement(self.quad)
        self.loadEnvironment()
        self.loadLights(self.shape, self.scene)

        self.setCameraPos()


        #key movement
        self.createKeyControls()
        self.defineIntervals()

        self.keyMap = {"left": 0, "right":0, "forward":0, "backward":0,
                        "turn-left":0, "turn-right":0, "turn-forward":0,
                        "turn-backward":0,}
        timer = 0.02
        taskMgr.doMethodLater(timer, self.move, "move")

    def loadModels(self):
        self.shape = loader.loadModel('models/isospherebaby2.x')
        self.shape.reparent_to(self.render)
        self.shape.setScale(20, 20, 20)
        self.shape.setPos(0, 0, 40)
        #self.shape.setHpr(2, 0, 90)



        self.quad = loader.loadModel('models/gridbacking5.x')
        self.quad.setPos(0, 0, 40)
        self.quad.setHpr(2, 0, 0)
        self.quad.setScale(3, 3, 3)


    # from panda3d docs
    def circularMovement(self, object):
        # can call on an object to give it cirular motion
        circle_center = render.attach_new_node('circle_center')
        circle_center.hprInterval(2, (-360,0,0)).loop()
        object.reparent_to(circle_center)

    def loadLights(self, object=None, environment=None):
        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        render.setLight(alnp)

        dirLight = DirectionalLight('directional')
        dirLight.setColor(Vec4(0.1, 0.4, 0.1, 1.0))
        dirNode = render.attachNewNode(dirLight)
        dirNode.setHpr(60, 0, 90)
        render.setLight(dirNode)

        dirLight1 = DirectionalLight('directional')
        dirLight1.setColor(Vec4(0.6, 0.4, 0.3, 0.7))
        dirNode1 = render.attachNewNode(dirLight1)
        dirNode1.setHpr(100, 0, 90)
        render.setLight(dirNode1)

        if object:
            sptLight = Spotlight('spot')
            sptLens = PerspectiveLens()
            sptLight.setLens(sptLens)
            sptLight.setColor(Vec4(1.0, 0.0, 0.0, 1.0))
            sptLight.setShadowCaster(True)
            sptNode = render.attachNewNode(sptLight)
            sptNode.setPos(200, 200, 200)
            sptNode.lookAt(object)
            render.setLight(sptNode)

        if environment:
            sptLight = Spotlight('spot')
            sptLens = PerspectiveLens()
            sptLight.setLens(sptLens)
            sptLight.setColor(Vec4(0.0, 0.7, 1.0, 1.0))
            sptLight.setShadowCaster(True)
            sptNode = render.attachNewNode(sptLight)
            sptNode.setPos(200, 200, 200)
            sptNode.lookAt(environment)
            render.setLight(sptNode)

    def loadEnvironment(self):
        # Load the environment model.
        self.scene = self.loader.loadModel("models/gridbacking5.x")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(20, 20, 20)
        self.scene.setPos(-8, 42, -100)
        self.scene.setHpr(90, 270, 0)

        # testing adding multiple environment models
        self.wall = self.loader.loadModel("models/gridbacking5.x")
        self.wall.reparentTo(self.render)
        self.wall.setScale(20, 20, 20)
        self.wall.setPos(-500, 42, 100)
        self.wall.setHpr(90, 0, 90)

    def setCameraPos(self):
        self.disable_mouse()
        #(x,y,z) = self.shape.getPos()
        self.camera.set_pos_hpr(500,-500,250,45,-22.5,0)
        #self.camera.reparent_to(self.shape)

    def setKey(self, key, value):
        self.keyMap[key] = value

    def createKeyControls(self):
        self.accept("r", self.doMovementLoop)

        #directional movement
        self.accept("arrow_up", self.setKey, ["forward", 1])
        self.accept("arrow_down", self.setKey, ["backward", 1])
        self.accept("arrow_left", self.setKey, ["left", 1])
        self.accept("arrow_right", self.setKey, ["right", 1])


        #directional movement - arrow up
        self.accept("arrow_up-up", self.setKey, ["forward", 0])
        self.accept("arrow_down-up", self.setKey, ["backward", 0])
        self.accept("arrow_left-up", self.setKey, ["left", 0])
        self.accept("arrow_right-up", self.setKey, ["right", 0])

        #turning movement
        self.accept("a", self.setKey, ["turn-left", 1])
        self.accept("d", self.setKey, ["turn-right", 1])
        self.accept("a-up", self.setKey, ["turn-left", 0])
        self.accept("d-up", self.setKey, ["turn-right", 0])

        # adds movement to make camera look up and down
        self.accept("w", self.setKey, ["turn-forward", 1])
        self.accept("s", self.setKey, ["turn-backward", 1])
        self.accept("w-up", self.setKey, ["turn-forward", 0])
        self.accept("s-up", self.setKey, ["turn-backward", 0])

    def move(self, task):
        (x, y, z) = self.shape.getPos()
        (h, p, r) = self.shape.getHpr()
        (ch, cp, cr) = self.camera.getHpr()

        if self.keyMap["forward"] > 0:
            (dx, dy, dz) = (1.8, 0, 0)
            (dh, dp, dr) = (0, 0, 0)

        elif self.keyMap["backward"] > 0:
            (dx, dy, dz) = (-1.8, 0, 0)
            (dh, dp, dr) = (0, 0, 0)

        elif self.keyMap["left"] > 0:
            (dx, dy, dz) = (0, 1.8, 0)
            (dh, dp, dr) = (0, 0, 0)

        elif self.keyMap["right"] > 0:
            (dx, dy, dz) = (0, -1.8, 0)
            (dh, dp, dr) = (0, 0, 0)

        elif self.keyMap["turn-left"] > 0:
            (dx, dy, dz) = (0, 0, 0)
            (dh, dp, dr) = (1.8, 0, 0)

        elif self.keyMap["turn-right"] > 0:
            (dx, dy, dz) = (0, 0, 0)
            (dh, dp, dr) = (-1.8, 0, 0)

        elif self.keyMap["turn-forward"] > 0:
            (dx, dy, dz) = (0, 0, 0)
            (dh, dp, dr) = (0, 1.8, 0)

        elif self.keyMap["turn-backward"] > 0:
            (dx, dy, dz) = (0, 0, 0)
            (dh, dp, dr) = (0, -1.8, 0)

        else:
            (dx, dy, dz) = (0, 0, 0)
            (dh, dp, dr) = (0, 0, 0)

        (newX, newY, newZ) = x + dx, y + dy, z + dz
        (newH, newP, newR) = h + dh, p + dp, r + dr
        (newCH, newCP, newCR) = ch + dh, cp + dp, cr + dr

        # update the positions & rotation
        self.shape.setX(newX)
        self.shape.setY(newY)
        self.shape.setZ(newZ)

        self.camera.setX(newX+500)
        self.camera.setY(newY-500)

        self.shape.setH(newH)
        self.shape.setP(newP)
        self.shape.setR(newR)

        #self.camera.setH(newH)
        self.camera.setP(newCP)

        return task.cont

    def defineIntervals(self):
        self.raceAround = Sequence(
            #self.shape.posInterval(2, (20, 0, 2)),
            #self.shape.hprInterval(1, (90, 0, 0)),
            #self.shape.posInterval(2, (0, 0, 2)),
            self.shape.hprInterval(2, (360, 360, 0))
            )

        self.jump = Sequence(
            self.shape.posInterval(0.5, (0, -4, 4)),
            self.shape.posInterval(0.5, (0, -4, 1)),
            )

        self.jumps = Sequence(self.jump, self.jump, self.jump, self.jump, self.jump)

    def doMovementLoop(self):
        '''
        loop = Parallel(
            self.raceAround
            #self.jumps
            )
        loop.start()
        '''
        self.raceAround.loop()

    def setVals(self, x, y):
        self.shape.setX(x)
        self.shape.setY(y)




action = TermProject()

def capp():
    cap = cv2.VideoCapture(0)
    while True:
        # _ is used to unpack values we don't want to use
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # Yellow - working
        lowerColY = np.array([20, 110, 110,])
        upperColY = np.array([40, 255, 255])
        yelMask = cv2.inRange(hsv, lowerColY, upperColY)


        # Blue - working
        lowerColB = np.array([100, 100, 120])
        upperColB = np.array([126, 255, 255])
        blueMask = cv2.inRange(hsv, lowerColB, upperColB)

        # Green - not done yet
        lowerColG = np.array([65, 60, 60])
        upperColG = np.array([80, 255, 255])
        greenMask = cv2.inRange(hsv, lowerColG, upperColG)

        # Red - not done yet



        # unpacks as two values instead of three because of cv2 versioning
        # finds blue objects
        (contours,_) = cv2.findContours(blueMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 800:
                x,y,w,h = cv2.boundingRect(contour)
                cx = x + (w//2)
                cy = y + (h//2)
                # changed to show center of object
                frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
                cv2.putText(frame,"Blue color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (255,0,0), 6)

                # prints coordinates of upper-left (x,y)
                # prints coordinates of center (x,y)
                #print('BLUE_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)


        # finds yellow objects
        (contours,_) = cv2.findContours(yelMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 800:
                x,y,w,h = cv2.boundingRect(contour)
                cx = x + (w//2)
                cy = y + (h//2)
                # changed to show center of object
                frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
                cv2.putText(frame,"Yellow color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (0,255,255), 6)

                # prints coordinates of upper-left (x,y)
                # prints coordinates of center (x,y)
                #print('YELLOW_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)

        # finds green objects
        (contours,_) = cv2.findContours(greenMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)

            if area > 800:
                x,y,w,h = cv2.boundingRect(contour)
                cx = x + (w//2)
                cy = y + (h//2)
                action.setVals(cx,cy)
                #action.setVals(cy)
                # changed to show center of object
                frame = cv2.rectangle(frame, (cx,cy),(x+w//2, y+h//2), (0,0,255), 10)
                cv2.putText(frame,"Green color",(x,y),cv2.FONT_HERSHEY_TRIPLEX, 2.0, (0,255,0), 6)

                # prints coordinates of upper-left (x,y)
                # prints coordinates of center (x,y)
                #print('GREEN_ ','UPL-X: ',x, 'UPL-Y: ', y , 'C-X: ', cx, 'C-Y', cy)

        cv2.imshow('tracking', frame)

        #cv2.imshow('c-tracking', cFrame)

        k = cv2.waitKey(5) & 0XFF

        if k == 27:
            break

        #green = np.uint8([[[0,0,255 ]]])
        #hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
        #print(hsv_green)
        cv2.destroyAllWindows()
        cap.release()

def game():
    base.run()

t1 = threading.Thread(target=capp, name='t1')
t2 = threading.Thread(target=game, name='game gui')

t1.start()
t2.start()

t1.join()
t2.join()
