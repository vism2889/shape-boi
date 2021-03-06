###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: Game.py
###############################################################################

# OLD WORKING VERSION OF GAME



## working character controller with collisions
# citation:
# https://docs.panda3d.org/1.10/python/programming/collision-detection/collision-solids
# https://arsthaumaturgis.github.io/Panda3DTutorial.io/tutorial/tut_lesson06.html




from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import Spotlight
from panda3d.core import Vec4
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode, CollisionBox
from panda3d.core import CollisionTube
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import Point3
import time
import subprocess
import socket
import threading
from direct.gui.DirectGui import DirectFrame
from panda3d.core import TextNode
from panda3d.core import OrthographicLens
from panda3d.core import TransparencyAttrib
from panda3d.core import NodePath

from Environment import *
#from panda3d.core import Font

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        base.setBackgroundColor(0.5,1,0.5)
        self.textObject = OnscreenText(text ='shape-boi', pos = (0.925,0.925), scale = 0.075)

        self.thread = threading.Thread(target=self.udpConnect)
        self.thread2 = threading.Thread(target=self.runColorTrack)
        self.connectButton = DirectButton(text=('Open Connection'),pos=(-0.3,0,-0.98), scale=0.090, command=self.openConnection, frameColor=(255,255,255,0.15))
        self.trackButton = DirectButton(text=('Color Track'),pos=(-1,0,-0.98), scale=0.090, command=self.thread2.start,frameColor=(255,255,255,0.15),state=0)
        self.connectButton.hide()
        self.trackButton.hide()
        self.scoreUI = OnscreenText(text = "0",
                                    pos = (-1.3, 0.825),
                                    mayChange = True,
                                    align = TextNode.ALeft)

        env = Environment("MorgansModels/mapTest2")
        #loader.loadModel("Models/Misc/environment")

        self.clientMsg = ''

        #render.setShaderAuto()
        #self.environment.setPos(0,54,-3)
        #self.environment.setH(90)
        #self.environment.setP(0)

        #self.environment.setScale(2)
        #self.environment.setZ(-10)


        self.tempActor = Actor("MorgansModels/shape-boi-grab-test-point_level2",
                                {"walk":"MorgansModels/shape-boi-grab-test-point_level2-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        '''
        # test with more realistic character
        self.tempActor = Actor("MorgansModels/mainCharacter_walking",
                                {"walk":"MorgansModels/mainCharacter_walking-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        '''
        self.tempActor.reparentTo(render)
        self.tempActor.setH(0)
        self.tempActor.setPos(0,54,-3)
        self.tempActor.setScale(0.5,0.5,0.5)
        self.tempActor.loop("walk")
        #player 1
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        colliderNode = CollisionNode("player")
        # Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
        colliderNode.addSolid(CollisionSphere(0,0,0, 0.8))
        collider = self.tempActor.attachNewNode(colliderNode)
        collider.show()
        base.pusher.addCollider(collider, self.tempActor)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher)
        self.pusher.setHorizontal(True)
        #collider.setZ(-3)

        self.myFriends = []
        for i in range(4):
            self.tempActor2 = Actor("MorgansModels/shape-boi-grab-test",
                                    {"walk":"MorgansModels/shape-boi-grab-test-ArmatureAction"})
            self.tempActor2.reparentTo(render)
            self.tempActor2.setH(180)
            self.tempActor2.setPos(0,50+(i*2),-3)
            self.tempActor2.setScale(0.5,0.5,0.5)
            self.tempActor2.loop("walk")
            self.myFriends.append(self.tempActor2)
        print(self.myFriends)




        self.score = 0


        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        # In the body of your code
        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        # Turn it around by 45 degrees, and tilt it down by 45 degrees
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)
        #render.setShaderAuto()
        '''
        liftSpot = Spotlight('spotlight')
        liftSpot.setColor((0.75, 1, 1, 1))
        self.spotLightNodePath = render.attachNewNode(liftSpot)
        render.setLight(self.spotLightNodePath)
        self.spotLightNodePath.setPos(self.tempActor2.getX(), self.tempActor2.getY(), self.tempActor2.getZ()+ 5)
        self.spotLightNodePath.lookAt(self.tempActor2)
        render.setShaderAuto()
        '''



        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False
            }
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("mouse1", self.updateKeyMap, ["shoot", True])
        self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])
        self.updateTask = taskMgr.add(self.update, "update")
        self.updateTask2 = taskMgr.add(self.updateScore, "updateScore")
        self.trackUpdate = taskMgr.add(self.handleMessage, 'handleMessage')
        #self.updateTask3 = taskMgr.add(self.udpUpdate)




        env.wallColliders()



        '''
        # towers
        wallSolid = CollisionTube(-1, 37, -4, -1, 37, 3, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()


        wallSolid = CollisionTube(-4.5, 48, -4, -4.5, 48, 3, 1)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()
        '''
        self.disableMouse()
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,6,4))
        #self.camera.setPos(0, 0, 50)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-12.5)

        self.friendRoomCam()

        self.startMenu()

    def friendRoomCam(self):
        self.leftCam = self.makeCamera(self.win, \
                            displayRegion = (0.79, 0.99, 0.01, 0.21), useCamera=None)
        self.leftCam.setZ(50)
        self.leftCam.setX(-18)
        self.leftCam.setY(118)
        self.leftCam.setP(-90)
        self.leftCam.reparentTo(render)

    def startMenu(self):
        self.font = loader.loadFont("Fonts/Wbxkomik.ttf")
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)

        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "shape-boi",
                            scale = 0.1,
                            pos = (0, 0, 0.6),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "saves his",
                             scale = 0.1,
                             pos = (0, 0, 0.4),
                             parent = self.titleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "friends",
                             scale = 0.125,
                             pos = (0, 0, 0.2),
                             parent = self.titleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))

        self.startButton = DirectButton(text=('StartGame'),pos=(0.5,0,0), scale=0.090, command=self.startGame, frameColor=(255,255,255,0.5))
        self.instructionsButton = DirectButton(text=('Instructions'),pos=(-0.5,0,0), scale=0.090, frameColor=(255,255,255,0.5))

    def startGame(self):
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.startButton.hide()
        self.instructionsButton.hide()
        if self.connectButton.isHidden():
            self.connectButton.show()
        if self.trackButton.isHidden():
            self.trackButton.show()

    def circularMovement(self, object):
        # can call on an object to give it cirular motion
        circle_center = render.attach_new_node('circle_center')
        circle_center.hprInterval(2, (-360,0,0)).loop()
        object.reparent_to(circle_center)

    def selectionLight(self, selection):
        vectorToObject = selection.getPos()-self.tempActor.getPos()
        vector2d = vectorToObject.getXy()
        distanceToObject = vector2d.length()
        ambient = AmbientLight('ambient')
        ambient.setColor((0.75, 0.75, 0.5, 1))
        ambientNP = selection.attachNewNode(ambient)

        if (distanceToObject < 0.65):
            print(distanceToObject, "selectionLight")

            selection.setLightOff()
            selection.setLight(ambientNP)
        else:
            #selection.getChildren().detach()
            selection.clearLight()
            selection.setLight(self.ambientLightNodePath)


    def pickUpObject(self):
        #for object in self.myFriends:
        vectorToObject = self.tempActor2.getPos()-self.tempActor.getPos()
        vector2d = vectorToObject.getXy()
        distanceToObject = vector2d.length()

        if distanceToObject < 0.6:
            #print(distanceToObject, "pickup")
            #self.selectionLight(self.tempActor2)
            self.tempActor2.setX(self.tempActor.getX() + 0.0)
            self.tempActor2.setY(self.tempActor.getY() + 0.25)
            self.tempActor2.setZ(self.tempActor.getZ() + 0.25)
            print(self.tempActor2.getY())


    def setObjectDown(self):
        #self.tempActor2.setX(self.tempActor2.getX() + 0.25)
        #self.tempActor2.setY(self.tempActor2.getY() + 0.25)
        self.tempActor2.setZ(-3)

    def cameraFollow(self):
        base.disableMouse()

        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,0,60))
        self.camera.setP(-90)
        #self.rightCam.setPos(self.tempActor.getPos()+ Vec3(0,12,4))
        #self.rightCam.setP(-12.5)
    def cameraSet(self):
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,-100,20))
        #self.camera.setPos(0, 0, 50)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-12.5)

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "set to", controlState)

    def openConnection(self):
        self.thread.start()
        self.trackButton['state'] = 1

    def handleMessage(self,task):
        dt = globalClock.getDt()
        msg = self.clientMsg
        (currX, currY) = (self.tempActor.getX(), self.tempActor.getY())
        # models movement instead of mirroring tracked objects (x,y)
        if msg == 'move_forward':
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_back':
            self.tempActor.setY(currY - 9*dt)
        elif msg == 'move_left':
            self.tempActor.setX(currX + 9*dt)
            #self.tempActor.setH(self.tempActor.getH() + 2)
        elif msg == 'move_right':
            self.tempActor.setX(currX - 9*dt)
        elif msg == 'move_forward_right':
            self.tempActor.setX(currX - 9*dt)
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_forward_left':
            self.tempActor.setX(currX + 9*dt)
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_back_right':
            self.tempActor.setX(currX - 9*dt)
            self.tempActor.setY(currY - 9*dt)
        elif msg == 'move_back_left':
            self.tempActor.setX(currX + 9*dt)
            self.tempActor.setY(currY - 9*dt)
        else:
            self.tempActor.setX(currX)
        return task.cont

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
            self.clientMsg = message.decode()
            clientIP  = "Client IP Address:{}".format(address)
            print('server listened message from client: ', self.clientMsg)
            #self.handleMessage(clientMsg, currX, currY)
            '''
            print(clientMsg[:].split(',')[0])
            #print(clientIP)
            cx = int(clientMsg[:].split(',')[0])
            self.shape.setX(-cx//2)
            cy = int(clientMsg[:].split(',')[1])
            self.shape.setY(-cy//2)
            '''

            # Sending a reply to client
            UDPServerSocket.sendto(bytesToSend, address)

    def runColorTrack(self):
        #useless_cat_call = subprocess.run(["python3", "/Users/morganvisnesky/shape_boi/colorTracker.py"], stdin=subprocess.PIPE, text=True)
        print('Running colorTracker.py...')

        proc = subprocess.Popen('python3 colorTracker.py', shell=True)

    def updateScore(self, task):
        self.scoreUI.setText('0')

        if (self.tempActor2.getX() > -37 and self.tempActor2.getX() < 0) \
            and (self.tempActor2.getY() > 110 and self.tempActor2.getY() < 132):
            print('scored')
            self.score +=1
            scoreString = str(self.score)
            self.scoreUI.setText(scoreString)
            return task.done
        else:
            return task.cont


    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        self.selectionLight(self.tempActor2)

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            #self.camera.setPos(self.tempActor.getPos())
            self.tempActor.setH(0)
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 9.0*dt, 0))

        if self.keyMap["down"]:
            self.tempActor.setH(180)
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -9.0*dt, 0))
        if self.keyMap["left"]:
            self.tempActor.setH(90)
            #self.tempActor.setR(self.tempActor.getR() + 2)
            #self.rightCam.setX(self.tempActor.getX()+5)
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-9.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setH(270)
            #self.rightCam.setX(self.tempActor.getX()+5)
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(9.0*dt, 0, 0))
        if self.keyMap["shoot"]:
            #self.score += 1
            #self.updateScore(self.score)

            self.cameraFollow()
            self.pickUpObject()

            #print ("Zap!")
        if self.keyMap["shoot"] == False:
            self.setObjectDown()
            self.cameraSet()
            #print ("Zap!")

        return task.cont

game = Game()
game.run()
