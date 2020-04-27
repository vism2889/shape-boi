###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: Game2.py
###############################################################################

# CURRENT WORKING VERSION OF GAME
## working character controller with collisions
# citation:
# https://docs.panda3d.org/1.10/python/programming/collision-detection/collision-solids
# https://arsthaumaturgis.github.io/Panda3DTutorial.io/tutorial/tut_lesson06.html
# font: http://webpagepublicity.com/free-fonts-y.html#Free%20Fonts year 2000 replicant
# http://www.mygamefast.com/volume1/issue7/3/ - second camera view



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
import sys
import signal
import os

from Environment import *
#from panda3d.core import Font

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        base.setBackgroundColor(0.5,1.0,0.75)
        self.lights()
        self.env = Environment("MorgansModels/mapTest2")
        self.env.wallColliders()
        self.env.plants()
        self.proc = None
        self.instanceNumber = 10
        self.rescueZone = Actor('MorgansModels/rescueZone-ArmatureAction.egg',
                                {"spin":"MorgansModels/rescueZone-ArmatureAction"})
        # holds a lot of possible locations to instance friend characters
        # so they dont get stuck in colliders
        self.possibleLocations = [(-30,77),(-19.7,44.2),(-29.89,26.36),(-9.72,46.73),
                                (29,56.54),(34.94,108.52),(24.95,88.33),(-22.3,102.55),
                                (-30.5,93.2),(19.48,92.78),(27.27,20.63),(-31.24,13.93)]
        #self.angle = 'camSet'
        # onscreen UI
        self.textObject = OnscreenText(text ='shape-boi', pos = (0.925,0.925), scale = 0.075,font=loader.loadFont('Fonts/Replicant.ttf'))
        self.scoreUI = OnscreenText(text = "Score: 0",
                                    pos = (-1.3, 0.825),
                                    mayChange = True,
                                    align = TextNode.ALeft,font=loader.loadFont('Fonts/Legion.ttf'), scale=0.05)
        self.countDownUI = OnscreenText(text = "",
                                    pos = (0.0, 0.925),
                                    mayChange = True,
                                    align = TextNode.ALeft,font=loader.loadFont('Fonts/Legion.ttf'), scale=0.05)


        self.thread = threading.Thread(target=self.udpConnect)
        self.thread2 = threading.Thread(target=self.runColorTrack)
        #loader.loadModel("Models/Misc/environment")
        self.mainCharacterModel = "MorgansModels/shape-boi-grab-test"
        self.clientMsg = ''
        self.carrying = False
        self.countDownTime = 120 # in seconds
        # test with more realistic character
        self.tempActor = Actor("MorgansModels/mainCharacter_walking",
                                {"walk":"MorgansModels/mainCharacter_walking-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})

        self.gameOver = True
        #self.keyMap = None
        self.keyMap = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False,
            "shoot" : False,
            "camera": False
            }
        self.accept("w", self.updateKeyMap, ["up", True])
        self.accept("w-up", self.updateKeyMap, ["up", False])
        self.accept("s", self.updateKeyMap, ["down", True])
        self.accept("s-up", self.updateKeyMap, ["down", False])
        self.accept("a", self.updateKeyMap, ["left", True])
        self.accept("a-up", self.updateKeyMap, ["left", False])
        self.accept("d", self.updateKeyMap, ["right", True])
        self.accept("d-up", self.updateKeyMap, ["right", False])
        self.accept("space", self.updateKeyMap, ["shoot", True])
        self.accept("space-up", self.updateKeyMap, ["shoot", False])
        self.accept("p", self.updateKeyMap, ["camera", True])
        self.accept("p-up", self.updateKeyMap, ["camera", False])
        self.updateTask = taskMgr.add(self.update, "update")




        #self.updateTask3 = taskMgr.add(self.udpUpdate)

        self.disableMouse()
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,6,4))
        #self.camera.setPos(0, 0, 50)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-12.5)

        self.friendRoomCam()

        self.startMenu()

        self.possibleCharacters = ['MorgansModels/shape-boi-grab-test',"MorgansModels/shape-boi-grab_char3","MorgansModels/shape-boi-grab_char2","MorgansModels/shape-boi-grab_char4","MorgansModels/shape-boi-grab_mrSpike", "MorgansModels/shape-boi-grab_mrSquare"]
        self.currIndexSelectionScreen = 0
        self.savedFriends = []
        self.myFriends = []
        self.score = len(self.savedFriends)
        self.instanceFriends()

        # winning background Music
        self.winSound = loader.loadSfx("sound/shapeboiSound2.ogg")
        self.winSound.setLoop(True)

        # normal backgroundMusic
        self.backSound = loader.loadSfx("sound/shapeboiSound.ogg")
        self.backSound.setLoop(True)
        self.backSound.play()



    def lights(self):
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

    def loadMainCharacter(self,mainCharModel):

        self.tempActor = Actor(mainCharModel,
                                {"walk":"MorgansModels/shape-boi-grab-test-point_level2-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
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
        colliderNode.addSolid(CollisionSphere(0,0,1, 1.7))
        collider = self.tempActor.attachNewNode(colliderNode)
        #collider.show()
        base.pusher.addCollider(collider, self.tempActor)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher)
        self.pusher.setHorizontal(True)
        #collider.setZ(-3)

    def changeActor(self, newActorModel):
        # got some help with this post
        # https://discourse.panda3d.org/t/replacing-model-in-actor/1447/5
        self.tempActor.removePart('modelRoot')
        self.tempActor.loadModel(newActorModel)

    def selectionScreenCharacterChange(self, currSelection):
        if self.currIndexSelectionScreen < (len(self.possibleCharacters)-1):
            self.currIndexSelectionScreen +=1
        else:
            self.currIndexSelectionScreen = 0
        newModel = self.possibleCharacters[self.currIndexSelectionScreen]
        self.mainCharacterModel = self.possibleCharacters[self.currIndexSelectionScreen]
        currSelection.removePart('modelRoot')
        currSelection.loadModel(newModel)
        #currSelection.loop("walk")

    def characterSelectionScreen(self):
        print('select screen')
        self.connectButton.hide()
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.startButton.hide()
        self.instructionsButton.hide()
        self.possibleActor = Actor("MorgansModels/shape-boi-grab-test-point_level2",
                                {"walk":"MorgansModels/shape-boi-grab-test-point_level2-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        '''
        # test with more realistic character
        self.tempActor = Actor("MorgansModels/mainCharacter_walking",
                                {"walk":"MorgansModels/mainCharacter_walking-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        '''
        self.possibleActor.reparentTo(render)
        self.possibleActor.setH(180)
        self.possibleActor.setPos(200,200,-3)
        self.possibleActor.setScale(0.5,0.5,0.5)
        #self.possibleActor.loop("walk")
        self.camera.setPos(self.possibleActor.getPos())
        self.camera.setZ(4)
        self.camera.setY(self.possibleActor.getY()-20)
        self.selectButton = DirectButton(text=('Change Character'),pos=(0.0,0,-0.75), scale=0.050, command=self.selectionScreenCharacterChange, extraArgs=[self.possibleActor],frameColor=(255,255,255,0.0),text_font=loader.loadFont('Fonts/Legion.ttf'))
        self.startButton2 = DirectButton(text=('StartGame'),pos=(0.0,0.0,0.75), scale=0.050, command=self.startGame, frameColor=(255,255,255,0.0),text_font=loader.loadFont('Fonts/Legion.ttf'))

        # scenery for selection menu
        self.shrub = loader.loadModel("MorgansModels/grass3")
        self.shrub.setPos(205,207,-3)
        self.shrub.setScale(4)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass3")
        self.shrub.setPos(195,207,-3)
        self.shrub.setScale(4)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass3")
        self.shrub.setPos(200,210,-3)
        self.shrub.setScale(6)
        self.shrub.setH(270)
        self.shrub.reparentTo(render)
        '''
        self.shrub = loader.loadModel("MorgansModels/mountains")
        self.shrub.setPos(195,240,-8)
        self.shrub.setScale(2.5)
        self.shrub.setH(0)
        self.shrub.reparentTo(render)
        '''

    def quitGame(self):
        sys.exit()
        #self.thread.exit()
        #self.thread2.exit()
        #self.UDPServerSocket.shutdown()
        #self.UDPServerSocket.close()

    def friendRoomCam(self):
        self.leftCam = self.makeCamera(self.win, \
                            displayRegion = (0.79, 0.99, 0.01, 0.21), useCamera=None)
        self.leftCam.setZ(50)
        self.leftCam.setX(-18)
        self.leftCam.setY(118)
        self.leftCam.setP(-90)
        self.leftCam.reparentTo(render)

    def instructions(self):
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.startButton.hide()
        self.instructionsButton.hide()
        self.connectButton.hide()
        self.font = loader.loadFont('Fonts/gone.ttf')
        self.font2 = loader.loadFont("Fonts/Legion.ttf")
        self.instructionsMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)

        self.instructionsMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "INSTRUCTIONS",
                            scale = 0.075,
                            pos = (0, 0, 0.8),
                            parent = self.instructionsMenu,
                            relief = None,
                            text_font = self.font2,
                            text_fg = (1, 1, 1, 1))

        title2 = DirectLabel(text = "Key Movement:",
                             scale = 0.05,
                             pos = (-1.2, 0, 0.4),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "W  -   forward",
                             scale = 0.05,
                             pos = (0.0, 0, 0.4),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "S  -   backward",
                             scale = 0.05,
                             pos = (0.0, 0, 0.3),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "A  -   left",
                             scale = 0.05,
                             pos = (0.0, 0, 0.2),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "D  -   right",
                             scale = 0.05,
                             pos = (0.0, 0, 0.1),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "Color-Tracking Movement:",
                             scale = 0.05,
                             pos = (-1.2, 0, 0.0),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "To enable color-tracking, click the color track button" + "\n" +"near the bottom of the window on the start page",
                             scale = 0.05,
                             pos = (-1.2, 0, -0.1),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = loader.loadFont('Fonts/gone.ttf'),
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "Actions:",
                             scale = 0.05,
                             pos = (-1.2, 0, -0.3),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "Spacebar  -   pick-up object (hold down to carry)",
                             scale = 0.05,
                             pos = (0.0, 0, -0.4),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "P  -   change camera view",
                             scale = 0.05,
                             pos = (0.0, 0, -0.5),
                             parent = self.instructionsMenu,
                             relief = None,
                             text_font = self.font,
                             text_align = TextNode.ALeft,
                             text_fg = (1, 1, 1, 1))

        self.returnToMenuButton = DirectButton(text=('BACK TO MENU'),pos=(0.0,0,-0.9), scale=0.090, command=self.showStartMenuHideInstructions, frameColor=(200,155,155,0.0), text_font=self.font2, text_fg=(0.5,0.5,0.75,1.0))
        #self.instructionsButton = DirectButton(text=('Instructions'),pos=(-0.5,0,0), scale=0.090, frameColor=(255,255,255,0.5), text_font=loader.loadFont('Fonts/Replicant.ttf'))
    def showStartMenuHideInstructions(self):
        self.titleMenu.show()
        self.titleMenuBackdrop.show()
        self.startButton.show()
        self.instructionsButton.show()
        self.connectButton.show()
        self.instructionsMenuBackdrop.hide()
        self.instructionsMenu.hide()
        self.returnToMenuButton.hide()

    def startMenu(self):
        self.font = loader.loadFont("Fonts/Gone.ttf")
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

        self.startButton = DirectButton(text=('StartGame'),pos=(0.5,0,0), scale=0.050, command=self.characterSelectionScreen, frameColor=(255,255,255,0.0), text_font=loader.loadFont('Fonts/Legion.ttf'),text_fg=(0.5,0.5,0.75,1.0))
        self.instructionsButton = DirectButton(text=('Instructions'),pos=(-0.5,0,0), scale=0.050, command=self.instructions,frameColor=(255,255,255,0.0), text_font=loader.loadFont('Fonts/Legion.ttf'),text_fg=(0.5,0.5,0.75,1.0))
        self.connectButton = DirectButton(text=('Color Track'),pos=(0.0,0,-0.7), scale=0.090, command=self.openConnection, frameColor=(255,255,255,0.0),text_font=loader.loadFont('Fonts/genotype.ttf'), text_fg=(255,255,255,1.0))
        #self.trackButton = DirectButton(text=('Color Track'),pos=(-1,0,-0.98), scale=0.090, command=self.thread2.start,frameColor=(255,255,255,0.0),state=0,text_font=loader.loadFont('Fonts/genotype.ttf'))

    def playAgainWin(self):
        self.cleanup()
        self.tempActor = Actor("MorgansModels/mainCharacter_walking",
                                {"walk":"MorgansModels/mainCharacter_walking-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        self.myFriends = []
        self.titleMenu.show()
        self.titleMenuBackdrop.show()
        self.startButton.show()
        self.instructionsButton.show()
        self.connectButton.show()
        self.restartButton.hide()
        self.quitButton.hide()
        self.winTitleMenu.hide()
        self.winSound.stop()
        self.backSound.play()

    def playAgainLose(self):
        self.cleanup()
        self.tempActor = Actor("MorgansModels/mainCharacter_walking",
                                {"walk":"MorgansModels/mainCharacter_walking-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        self.myFriends = []
        self.titleMenu.show()
        self.titleMenuBackdrop.show()
        self.startButton.show()
        self.instructionsButton.show()
        self.connectButton.show()
        self.restartButton.hide()
        self.quitButton.hide()
        self.loseTitleMenu.hide()
        #self.winSound.stop()
        #self.backSound.play()

    def cleanup(self):
        self.gameOver = True
        for friend in self.savedFriends:
            friend.cleanup()

        self.savedFriends = []
        for friend in self.myFriends:
            friend.cleanup()

        self.myFriends = []
        self.possibleActor.cleanup()
        if self.tempActor is not None:
            self.tempActor.cleanup()
            #self.tempActor = None
        self.rescueZone.cleanup()
        self.score = 0
        self.countDownTime = 120
        scoreString = str(self.score)
        self.scoreUI.setText('Score: ' +scoreString)
        self.countDownUI.setText('')

    def instanceFriends(self):
        for i in range(self.instanceNumber):
            # this loop adds friends
            (x,y) = random.choice(self.possibleLocations)
            character = random.choice(self.possibleCharacters)
            self.tempActor2 = Actor(character,
                                    {"walk":"MorgansModels/shape-boi-grab-test-ArmatureAction"})
            self.tempActor2.reparentTo(render)
            self.tempActor2.setH(180)
            self.tempActor2.setPos(x,y,-3)
            self.tempActor2.setScale(0.5,0.5,0.5)
            self.tempActor2.loop("walk")
            self.myFriends.append(self.tempActor2)
            print(self.myFriends)

    def startGame(self):
        self.cleanup()
        self.gameOver = False
        self.updateTask2 = taskMgr.add(self.updateScore, "updateScore")
        self.trackUpdate = taskMgr.add(self.handleMessage, 'handleMessage')
        #self.trackUpdate = taskMgr.add(self.changeBackgroundColor, 'changeBackgroundColor')
        self.instanceFriends()
        self.loadMainCharacter(self.mainCharacterModel)
        self.startButton2.hide()
        self.selectButton.hide()
        self.connectButton.hide()
        self.cameraSet()

        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.startButton.hide()
        self.instructionsButton.hide()
        if self.connectButton.isHidden():
            self.connectButton.hide()
        self.rescueZone = Actor('MorgansModels/rescueZone',
                                {"walk":"MorgansModels/rescueZone-ArmatureAction"})
        self.rescueZone.reparentTo(render)
        self.rescueZone.setH(0)
        self.rescueZone.setPos(-17,120,3)
        self.rescueZone.setScale(2.5,2.5,2.5)
        self.rescueZone.loop("walk")
        #if self.trackButton.isHidden():
        #    self.trackButton.show()
        #self.restartButton = DirectButton(text=('Play Again'),pos=(0.0,0,-0.9), scale=0.090,command=self.playAgain,frameColor=(255,255,255,0.5),text_font=self.font)
        self.timerUpdate = taskMgr.doMethodLater(1.0, self.clockUpdate, 'handleMessage')

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
            #print(distanceToObject, "selectionLight")

            selection.setLightOff()
            selection.setLight(ambientNP)
        else:
            #selection.getChildren().detach()
            selection.clearLight()
            selection.setLight(self.ambientLightNodePath)


    def pickUpObject(self):
        for object in self.myFriends:
            vectorToObject = object.getPos()-self.tempActor.getPos()
            vector2d = vectorToObject.getXy()
            distanceToObject = vector2d.length()

            if distanceToObject < 1.25:
                object.setX(self.tempActor.getX() + 0.0)
                object.setY(self.tempActor.getY() + 0.25)
                object.setZ(self.tempActor.getZ() + 0.25)


    def setObjectDown(self):
        for object in self.myFriends:
            vectorToObject = object.getPos()-self.tempActor.getPos()
            vector2d = vectorToObject.getXy()
            distanceToObject = vector2d.length()

            if distanceToObject < 1.25:
                object.setZ(-3)
                #self.carrying = False

    def cameraFollow(self):
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,0,60))
        self.camera.setP(-90)

    def cameraSet(self):
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,-100,20))
        self.camera.setP(-12.5)

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        #print (controlName, "set to", controlState)

    def openConnection(self):
        self.thread.start()
        #self.trackButton['state'] = 1 # used to disable track button until UDPconnect button is pressed
        self.thread2.start()

    def handleMessage(self,task):
        dt = globalClock.getDt()
        msg = self.clientMsg
        (currX, currY) = (self.tempActor.getX(), self.tempActor.getY())
        # models movement instead of mirroring tracked objects (x,y)
        if msg == 'move_forward':
            self.tempActor.setH(0)
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_back':
            self.tempActor.setH(180)
            self.tempActor.setY(currY - 9*dt)
        elif msg == 'move_left':
            self.tempActor.setH(270)
            self.tempActor.setX(currX + 9*dt)
        elif msg == 'move_right':
            self.tempActor.setH(90)
            self.tempActor.setX(currX - 9*dt)
        elif msg == 'move_forward_right':
            self.tempActor.setH(45)
            self.tempActor.setX(currX - 9*dt)
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_forward_left':
            self.tempActor.setH(315)
            self.tempActor.setX(currX + 9*dt)
            self.tempActor.setY(currY + 9*dt)
        elif msg == 'move_back_right':
            self.tempActor.setH(135)
            self.tempActor.setX(currX - 9*dt)
            self.tempActor.setY(currY - 9*dt)
        elif msg == 'move_back_left':
            self.tempActor.setH(225)
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
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((localIP, localPort))
        print("UDP server up and listening")
        while(True):
            bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            self.clientMsg = message.decode()
            clientIP  = "Client IP Address:{}".format(address)
            print('server listened message from client: ', self.clientMsg)
            #self.handleMessage(clientMsg, currX, currY)
            '''
            # using (x,y) to control characters movement
            print(clientMsg[:].split(',')[0])
            #print(clientIP)
            cx = int(clientMsg[:].split(',')[0])
            self.shape.setX(-cx//2)
            cy = int(clientMsg[:].split(',')[1])
            self.shape.setY(-cy//2)
            '''
            # Sending a reply to client
            self.UDPServerSocket.sendto(bytesToSend, address)

    def runColorTrack(self):
        print('Running colorTracker.py...')
        self.proc = subprocess.Popen('python3 colorTracker.py', shell=True)

    def killColorTrack(self):
        self.proc.kill()
        self.proc.kill()

    def gameOverWin(self):
        #self.gameOver = True
        # UI that is displayed when a win occurs
        self.connectButton.hide()
        #self.trackButton.hide()
        self.font = loader.loadFont("Fonts/Gone.ttf")
        #self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             #frameSize = (-1, 1, -1, 1),
                                             #parent = render2d)

        self.winTitleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "You Won!",
                            scale = 0.1,
                            pos = (0, 0, 0.6),
                            parent = self.winTitleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = "Thanks for helping SHAPE BOI!",
                             scale = 0.1,
                             pos = (0, 0, 0.4),
                             parent = self.winTitleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "Play Again?",
                             scale = 0.125,
                             pos = (0, 0, 0.2),
                             parent = self.winTitleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))

        self.restartButton = DirectButton(text=('Play Again'),pos=(0.5,0,0), scale=0.090,command=self.playAgainWin,frameColor=(255,255,255,0.5),text_font=self.font)
        self.quitButton = DirectButton(text=('Quit Game'),pos=(-0.5,0,0), scale=0.090, command=self.quitGame,frameColor=(255,255,255,0.5),text_font=self.font)
        #self.titleMenuBackdrop.hide()
        #self.titleMenu.hide()
        #self.restartButton.hide()
        #self.quitButton.hide()
        #self.WintitleMenu.show()
        self.backSound.stop()
        self.winSound.play()

    def gameOverLose(self):
        #self.gameOver = True
        # UI that is displayed when a win occurs
        self.connectButton.hide()
        #self.trackButton.hide()
        self.font = loader.loadFont("Fonts/gone.ttf")
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                             frameSize = (-1, 1, -1, 1),
                                             parent = render2d)

        self.loseTitleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "GAME OVER",
                            scale = 0.1,
                            pos = (0, 0, 0.6),
                            parent = self.loseTitleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg = (1, 1, 1, 1))
        title2 = DirectLabel(text = str(len(self.myFriends)) + " friends are still sad",
                             scale = 0.1,
                             pos = (0, 0, 0.4),
                             parent = self.loseTitleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))
        title3 = DirectLabel(text = "Play Again?",
                             scale = 0.125,
                             pos = (0, 0, 0.2),
                             parent = self.loseTitleMenu,
                             relief = None,
                             text_font = self.font,
                             text_fg = (1, 1, 1, 1))

        self.restartButton = DirectButton(text=('Play Again'),pos=(0.5,0,0), scale=0.090,command=self.playAgainLose, frameColor=(255,255,255,0.5),text_font=self.font)
        self.quitButton = DirectButton(text=('Quit Game'),pos=(-0.5,0,0), scale=0.090, command=self.quitGame, frameColor=(255,255,255,0.5),text_font=self.font)
        #self.titleMenuBackdrop.hide()
        #self.titleMenu.hide()
        #self.restartButton.hide()
        #self.quitButton.hide()

    def updateScore(self, task):
        #self.scoreUI.setText('0')
        if self.countDownTime <= 0:
            self.gameOverLose()
            return task.done
        if len(self.myFriends) > 0:
            for friend in self.myFriends:
                if (friend.getX() > -37 and friend.getX() < -10) \
                    and (friend.getY() > 110 and friend.getY() < 132):
                    print('scored')
                    self.savedFriends.append(friend)
                    self.score = len(self.savedFriends)
                    scoreString = str(self.score)
                    self.scoreUI.setText('Score: ' +scoreString)
                    self.myFriends.remove(friend)
            return task.cont
        elif self.score == self.instanceNumber:
            self.gameOverWin()
        else:
            return task.done

    def clockUpdate(self, task):
        if self.score == self.instanceNumber:
            return task.done
        if self.countDownTime >= 0:
            minutes = self.countDownTime // 60
            seconds = self.countDownTime % 60
            if seconds < 10:
                seconds = "0"+ str(seconds)
            self.countDownUI.setText(str(minutes)+ ' : ' + str(seconds))
            self.countDownTime -=1
            return task.again
        else:
            return task.done





    def changeCameraAngle(self):
        if self.angle == 'camFollow':
            self.cameraSet()
        if self.angle == 'camSet':
            self.cameraFollow()


    def update(self, task):

        # Get the amount of time since the last update
        dt = globalClock.getDt()
        # iterates over friends list to check if they need a selection light applied
        for i in range(len(self.myFriends)):
            self.selectionLight(self.myFriends[i])
        for i in range(len(self.savedFriends)):
            self.savedFriends[i].clearLight()
            self.savedFriends[i].setLight(self.ambientLightNodePath)


        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.tempActor.setH(0) # changes to face direction of movement
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 13.0*dt, 0))
        if self.keyMap["down"]:
            self.tempActor.setH(180) # changes to face direction of movement
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -13.0*dt, 0))
        if self.keyMap["left"]:
            self.tempActor.setH(90) # changes to face direction of movement
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-13.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setH(270) # changes to face direction of movement
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(13.0*dt, 0, 0))
        if self.keyMap["shoot"] and self.gameOver == False:
            #self.cameraFollow()
            self.pickUpObject()

            #self.changeActor("MorgansModels/mainCharacter_walking")

        if self.keyMap["shoot"] == False and self.gameOver == False:
            self.setObjectDown()
            #self.cameraSet()

        if self.keyMap["camera"]:
            #self.setObjectDown()
            self.cameraFollow()
            #self.changeCameraAngle()
        if self.keyMap["camera"] == False and self.gameOver == False:
            #self.setObjectDown()
            self.cameraSet()
            #self.changeCameraAngle()
        #print(self.tempActor.getX(), self.tempActor.getY())
        return task.cont




game = Game()
game.run()
