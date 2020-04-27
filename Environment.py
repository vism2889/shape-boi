###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: Environment.py
###############################################################################


# class to set up environment models and most other static game objects
# lighting, colliders that correspond to the map walls, more TBD


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
import random
import threading
from direct.gui.DirectGui import DirectFrame
from panda3d.core import TextNode
from panda3d.core import OrthographicLens
from panda3d.core import TransparencyAttrib
from panda3d.core import NodePath

class Environment():
    def __init__(self, model):
        '''
            Loads model for ground and walls of the environment and sets
            position, and orientation.
        '''
        self.environment = loader.loadModel(model)
        self.environment.setPos(0,54,-3)
        self.environment.setH(90)
        self.environment.setP(0)
        self.environment.reparentTo(render)
        #nodePath = NodePath(self.environment)
        #nodePath.setTransparency(TransparencyAttrib.MAlpha)
        #nodePath.reparentTo(render)
        #return 42

    def plants(self):
        '''
            Creates trees and other plant-like game objects.
        '''
        self.tree1 = loader.loadModel("MorgansModels/tree_one")
        self.tree1.setPos(-20,54,-3)
        self.tree1.setScale(3)
        self.tree1.reparentTo(render)


        self.tree2 = loader.loadModel("MorgansModels/tree_two")
        self.tree2.setPos(-30,20,-3)
        self.tree2.setScale(3)
        self.tree2.reparentTo(render)

        self.tree3 = loader.loadModel("MorgansModels/tree_three")
        self.tree3.setPos(30,75,-3)
        self.tree3.setScale(3)
        self.tree3.setH(90)
        self.tree3.reparentTo(render)

        self.tree4 = loader.loadModel("MorgansModels/tree_three")
        self.tree4.setPos(-35,100,-3)
        self.tree4.setScale(3)
        self.tree4.setH(90)
        self.tree4.reparentTo(render)

        self.seaShell = loader.loadModel("MorgansModels/seashell")
        self.seaShell.setPos(33,120,-3)
        self.seaShell.setScale(3)
        self.seaShell.setH(90)
        self.seaShell.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub")
        self.shrub.setPos(35,127,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub2")
        self.shrub.setPos(35,114,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)

        self.tree4 = loader.loadModel("MorgansModels/tree_two")
        self.tree4.setPos(29,129,-3)
        self.tree4.setScale(6)
        self.tree4.setH(90)
        self.tree4.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub2")
        self.shrub.setPos(27,129,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)

        # shrub rows

        for i in range(8):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-35+i*5,105,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30+15)
            self.shrub.reparentTo(render)

        for i in range(7):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-35+i*5,130,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30+15)
            self.shrub.reparentTo(render)

        for i in range(7):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-35+i*5,112,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30+15)
            self.shrub.reparentTo(render)
        '''
        self.shrub = loader.loadModel("MorgansModels/shrub2")
        self.shrub.setPos(-35,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub")
        self.shrub.setPos(-30,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub2")
        self.shrub.setPos(-25,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(270)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub")
        self.shrub.setPos(-20,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub2")
        self.shrub.setPos(-15,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(160)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/shrub")
        self.shrub.setPos(-10,105,-3)
        self.shrub.setScale(2)
        self.shrub.setH(240)
        self.shrub.reparentTo(render)
        '''
        for i in range(18):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-35,95-i*5,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30)
            self.shrub.reparentTo(render)

        for i in range(7):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-10,70-i*5,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30)
            self.shrub.reparentTo(render)

        for i in range(4):
            model = ''
            if i % 2 == 0:
                model = "MorgansModels/shrub"
            else:
                model = "MorgansModels/shrub2"
            self.shrub = loader.loadModel(model)
            self.shrub.setPos(-10+i*5,35,-3)
            self.shrub.setScale(2)
            self.shrub.setH(90+i*30)
            self.shrub.reparentTo(render)


        # grass
        self.shrub = loader.loadModel("MorgansModels/grass1")
        self.shrub.setPos(20,75,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass1")
        self.shrub.setPos(20.5,75,-3)
        self.shrub.setScale(1.5)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(20,95,-3)
        self.shrub.setScale(5)
        self.shrub.setH(0)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass1")
        self.shrub.setPos(20.5,85,-3)
        self.shrub.setScale(1.5)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        # grass by big tree, right side of map
        self.shrub = loader.loadModel("MorgansModels/grass1")
        self.shrub.setPos(30,73.5,-3)
        self.shrub.setScale(2)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass1")
        self.shrub.setPos(30.5,73.5,-3)
        self.shrub.setScale(1.5)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(30,53.5,-3)
        self.shrub.setScale(5)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(25.5,53.5,-3)
        self.shrub.setScale(1.5)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)


        # grass on left side of map
        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(-30,73.5,-3)
        self.shrub.setScale(4)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(-30.5,73.5,-3)
        self.shrub.setScale(2)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass3")
        self.shrub.setPos(-20,40.5,-3)
        self.shrub.setScale(4)
        self.shrub.setH(90)
        self.shrub.reparentTo(render)
        self.shrub = loader.loadModel("MorgansModels/grass2")
        self.shrub.setPos(-24.5,43.5,-3)
        self.shrub.setScale(2)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        self.shrub = loader.loadModel("MorgansModels/grass3")
        self.shrub.setPos(34,110,-3)
        self.shrub.setScale(4)
        self.shrub.setH(180)
        self.shrub.reparentTo(render)

        for i in range(1,30,4):
            for j in range(1,40,4):
                x = random.randint(0,30)
                y = random.randint(0,40)
                randScale = random.randint(1,3)
                self.shrub = loader.loadModel("MorgansModels/grass2")
                self.shrub.setPos(9.5+x,8.7+y,-3)
                if i % 2 == 0:
                    self.shrub.setScale(randScale)
                if i % 5 == 0:
                    self.shrub.setScale(randScale)
                if i % 3 == 0 and j % 3 == 0:
                    self.shrub.setScale(2.)
                self.shrub.setH(180+(i*j))
                self.shrub.reparentTo(render)


        for i in range(1,50,4):
            for j in range(1,40,4):
                x = random.randint(0,50)
                y = random.randint(0,40)
                randScale = random.randint(1,4)
                self.shrub = loader.loadModel("MorgansModels/grass2")
                self.shrub.setPos(-30+x,72+y,-3)
                if i % 2 == 0:
                    self.shrub.setScale(randScale)
                if i % 5 == 0:
                    self.shrub.setScale(randScale)
                if i % 3 == 0 and j % 3 == 0:
                    self.shrub.setScale(2.)
                self.shrub.setH(180+(i*j))
                self.shrub.reparentTo(render)


    def wallColliders(self):
        '''
            Creates and postions colliders that correspond to the walls of
            the game map.
        '''
        # walls
        wallSolid = CollisionTube(-7.0, 39, -2, 7, 39, -2, 1.2)
        #wallSolid = CollisionBox(Point3(-5,64,-4), Point3(2.5, 2.5, 0.25))
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        #wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-2.0, 61, -2, 7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-7.0, 30, -2, -7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(7.0, 40, -2, 7, 61, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-38, -1, -2, -38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(38, -1, -2, 38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-38, 124, -2, 38, 124, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-38, -1, -2, 38, -1, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(-38, 101, -2, 0, 101, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(1, 101, -2, 1, 114, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(22.5, 62, -2, 22.5, 93, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()

        wallSolid = CollisionTube(8, 92.5, -2, 22.5, 92.5, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        #wall.show()
