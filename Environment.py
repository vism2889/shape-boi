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

class Environment():
    def __init__(self, model):
        self.environment = loader.loadModel(model)
        self.environment.setPos(0,54,-3)
        self.environment.setH(90)
        self.environment.setP(0)
        self.environment.reparentTo(render)
        #nodePath = NodePath(self.environment)
        #nodePath.setTransparency(TransparencyAttrib.MAlpha)
        #nodePath.reparentTo(render)
        #return 42

    def walls(self):
        # walls
        wallSolid = CollisionTube(-7.0, 39, -2, 7, 39, -2, 1.2)
        #wallSolid = CollisionBox(Point3(-5,64,-4), Point3(2.5, 2.5, 0.25))
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        #wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-2.0, 61, -2, 7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-7.0, 30, -2, -7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(7.0, 40, -2, 7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-38, -1, -2, -38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(38, -1, -2, 38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-38, 124, -2, 38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-38, -1, -2, 38, -1, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-38, 101, -2, 0, 101, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(1, 101, -2, 1, 114, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(22.5, 62, -2, 22.5, 93, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(8, 92.5, -2, 22.5, 92.5, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()
