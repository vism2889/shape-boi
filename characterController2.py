from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from direct.actor.Actor import Actor
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
from panda3d.core import CollisionTraverser
from direct.task import Task



#from panda3d.core import Shader

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        base.enableParticles()
        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)


        self.environment = loader.loadModel("mirroredwalltest.x")
        self.environment.reparentTo(render)
        self.environment.getChild(0).setHpr(180)
        self.environment.getChild(0).setPos(0,50,-5)

        self.shape = loader.loadModel("isospherebaby2.x")
        self.shape.setPos(0,50,0)
        self.shape.reparentTo(render)

        self.camera.setPos(0,-100,50)
        self.camera.setP(-90)


        # LIGHTS
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


        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, -4.75)))
        pnodePath = self.shape.attachNewNode(CollisionNode('pnode'))
        pnodePath.node().addSolid(plane)
        pnodePath.show()





        gravityFN=ForceNode('world-forces')
        gravityFNP=render.attachNewNode(gravityFN)
        gravityForce=LinearVectorForce(0,0,-9.81) #gravity acceleration
        gravityFN.addForce(gravityForce)

        node = NodePath("PhysicsNode")
        node.reparentTo(self.render)
        an = ActorNode("jetpack-guy-physics")
        anp = node.attachNewNode(an)
        base.physicsMgr.attachPhysicalNode(an)
        jetpackGuy = loader.loadModel("isospherebaby2.x")
        jetpackGuy.reparentTo(anp)
        jetpackGuy.setPos(0,50,10)
        cs = CollisionSphere(0, 0, 0, 2.3)
        cnodePath = jetpackGuy.attachNewNode(CollisionNode('jpgnode'))
        cnodePath.node().addSolid(cs)
        cnodePath.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        cnodePath.show()

        lifter = CollisionHandlerFloor()
        lifter.setMaxVelocity(15)
        lifter.setOffset(1.0)
        lifter.addCollider(cnodePath, pnodePath)

        an.getPhysicsObject().setMass(16.077)   # about 300 lbs


        base.physicsMgr.addLinearForce(gravityForce)

        self.cTrav = CollisionTraverser()
        queue = CollisionHandlerQueue()
        hevent = CollisionHandlerEvent()
        self.cTrav.addCollider(cnodePath, queue)
        self.cTrav.addCollider(pnodePath, queue)
        self.cTrav.traverse(render)

        for entry in queue.getEntries():
            print(entry)
    # This task runs for two seconds, then prints done
    def exampleTask(task):
        if task.time < 2.0:
            return Task.cont

        print('Done')
        return Task.done

game = Game()
game.run()
