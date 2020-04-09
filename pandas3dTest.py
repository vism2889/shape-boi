###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: pandas3dTest.py
###############################################################################
'''
    - Trial run of loading and animating own models exported from blender
    -
'''
# Citations:
#   - Patricks TA-led mini lecture / panda3D starter file 
#   - https://discourse.panda3d.org/t/moving-setting-camera-pos-at-start-solved/2941 - cameraPos
#
#
# TODO:
#   - Normalize (cx,cy) vals
#   - Find a way to exit colortracking subprocess when game closes
#   - Game object collisions
#   - Background Music / Sound FX

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
#textObject = OnscreenText(text='my text string', pos=(-0.5, 0.02), scale=0.07)

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
import subprocess
import socket
import threading
from panda3d.bullet import BulletWorld
#from panda3d.core import Shader

objX = 0
objY = 0

class TermProject(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        '''
        myShader = Shader.load(Shader.SL_GLSL,
                       vertex="test.vert",
                       fragment="test.frag",
                       geometry="test.geom")
                       '''
        self.loadModels()
        #self.shape.set_shader(myShader)
        #self.circularMovement(self.shape)
        #self.circularMovement(self.quad)
        self.loadEnvironment()
        self.loadLights(self.shape, self.scene)

        #tweetText = TextNode('new tweet text')
        #tweetText.setText('New Tweet!')
        #textNodePath = aspect2d.attachNewNode(tweetText)
        #textNodePath.setScale(0.07)
        #OnscreenText(text='my text string', pos=(-0.5, 0.02), scale=0.07)
        self.textObject = OnscreenText(text ='shape-boi', pos = (0.925,0.925), scale = 0.075)

        #self.cb = DirectCheckButton(text = "CheckButton" ,scale=.05,command=self.doMovementLoop)
        self.setCameraPos()
        #self.udpConnect()
        #key movement
        self.thread = threading.Thread(target=self.udpConnect)
        self.thread2 = threading.Thread(target=self.runColorTrack)
        #thread.start()
        #thread2.start()
        self.connectButton = DirectButton(text=('Open Connection'),pos=(-0.3,0,-0.98), scale=0.090, command=self.openConnection, frameColor=(255,255,255,0.15))
        self.trackButton = DirectButton(text=('Color Track'),pos=(-1,0,-0.98), scale=0.090, command=self.thread2.start,frameColor=(255,255,255,0.15),state=0)

        self.createKeyControls()
        self.defineIntervals()


        self.keyMap = {"left": 0, "right":0, "forward":0, "backward":0,
                        "turn-left":0, "turn-right":0, "turn-forward":0,
                        "turn-backward":0,}
        timer = 0.02
        taskMgr.doMethodLater(timer, self.move, "move")

    def openConnection(self):
        self.thread.start()
        self.trackButton['state'] = 1


    def udpConnect(self):
        localIP     = "127.0.0.1"
        localPort   = 20001
        bufferSize  = 1024
        msgFromServer       = "Hello UDP Client"
        bytesToSend         = str.encode(msgFromServer)
        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        UDPServerSocket.bind((localIP, localPort))

        print("UDP server up and listening")
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            clientMsg = message.decode()
            clientIP  = "Client IP Address:{}".format(address)
            print(clientMsg[:].split(',')[0])
            #print(clientIP)
            cx = int(clientMsg[:].split(',')[0])
            self.shape.setX(-cx//2)
            cy = int(clientMsg[:].split(',')[1])
            self.shape.setY(-cy//2)



            # Sending a reply to client

            UDPServerSocket.sendto(bytesToSend, address)
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
    def stopMovementLoop(self):
        '''
        loop = Parallel(
            self.raceAround
            #self.jumps
            )
        loop.start()
        '''
        self.raceAround.loop()

    def runColorTrack(self):
        #useless_cat_call = subprocess.run(["python3", "/Users/morganvisnesky/shape_boi/colorTracker.py"], stdin=subprocess.PIPE, text=True)
        print('Running colorTracker.py...')

        proc = subprocess.Popen('python3 colorTracker.py', shell=True)



            #pass
        #print(useless_cat_call.stdout)
        #self.shape.setX(int(useless_cat_call.stdout))
action = TermProject()
base.run()
