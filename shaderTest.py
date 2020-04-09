###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: shaderTest.py
###############################################################################
'''
    - Trial run of loading and using GLSL shaders written initially for kodelife
    -
'''
# Citations:
#   - Previous experience with GLSL
#   - https://docs.panda3d.org/1.10/python/programming/shaders/shader-basics
#
#

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



class ShaderTest(ShowBase):
    def __intit__(self):
        ShowBase.__init__(self)
        self.shape = loader.loadModel('models/gridbacking5.x')
        self.shape.reparent_to(self.render)
        self.shape.setScale(20, 20, 20)
        self.shape.setPos(0, 0, 40)

        #self.camera.setPos(10,10,0)
        self.disable_mouse()
        self.camera.reparentTo(self.shape)
        alight = AmbientLight('alight')
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(alight)
        self.render.setLight(alnp)

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

action = ShaderTest()
base.run()
