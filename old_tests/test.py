###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: test.py
###############################################################################


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

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.textObject = OnscreenText(text ='shape-boi', pos = (0.925,0.925), scale = 0.075)

        #self.thread = threading.Thread(target=self.udpConnect)
        #self.thread2 = threading.Thread(target=self.runColorTrack)
        #self.connectButton = DirectButton(text=('Open Connection'),pos=(-0.3,0,-0.98), scale=0.090, command=self.openConnection, frameColor=(255,255,255,0.15))
        #self.trackButton = DirectButton(text=('Color Track'),pos=(-1,0,-0.98), scale=0.090, command=self.thread2.start,frameColor=(255,255,255,0.15),state=0)



        #loader.loadModel("Models/Misc/environment")
        self.environment = loader.loadModel("MorgansModels/mirroredwalltest.x")
        self.environment.reparentTo(render)
        self.environment.getChild(0).setPos(0,50,-4)
        self.environment.getChild(0).setH(90)
        self.environment.getChild(0).setP(0)


        self.tempActor = Actor("MorgansModels/shape-boi-grab-test-point_level2",
                                {"walk":"MorgansModels/shape-boi-grab-test-point_level2-ArmatureAction",
                                 "lift":"MorgansModels/shape-boi-grab-test-point_level2-IcosphereAction"})
        self.tempActor.reparentTo(render)
        self.tempActor.getChild(0).setH(180)
        self.tempActor.getChild(0).setPos(0,54,-3)
        self.tempActor.getChild(0).setScale(0.5,0.5,0.5)
        self.tempActor.loop("walk")

        self.tempActor2 = Actor("MorgansModels/shape-boi-grab-test",
                                {"walk":"MorgansModels/shape-boi-grab-test-ArmatureAction"})
        self.tempActor2.reparentTo(render)
        self.tempActor2.getChild(0).setH(180)
        self.tempActor2.getChild(0).setPos(1,54,-3)
        self.tempActor2.getChild(0).setScale(0.5,0.5,0.5)
        self.tempActor2.loop("walk")


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
        render.setShaderAuto()




game = Game()
game.run()
