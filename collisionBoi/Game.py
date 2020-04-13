from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import Vec4
from direct.actor.Actor import Actor
from panda3d.core import DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionTube
from GameObjects import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.player = Player()

        self.tempEnemy = WalkingEnemy(Vec3(5, 0, 0))
        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        #loader.loadModel("Models/Misc/environment")
        self.environment = loader.loadModel("mirroredwalltest.x")
        self.environment.reparentTo(render)
        self.environment.getChild(0).setPos(0,50,-4)
        self.environment.getChild(0).setH(90)
        self.environment.getChild(0).setP(0)

        base.disableMouse()
        self.camera.setPos(0, 0, 50)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-45)
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





        # walls
        wallSolid = CollisionTube(-10.0, 32, -2, 10, 32, -2, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-10.0, 51, -2, 10, 51, -2, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-8.0, 30, -2, -8, 55, -2, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(8.0, 30, -2, 8, 55, -2, 0.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()


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






    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "set to", controlState)

    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, 5.0*dt, 0))
        if self.keyMap["down"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(0, -5.0*dt, 0))
        if self.keyMap["left"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(-5.0*dt, 0, 0))
        if self.keyMap["right"]:
            self.tempActor.setPos(self.tempActor.getPos() + Vec3(5.0*dt, 0, 0))
        if self.keyMap["shoot"]:
            print ("Zap!")
        return task.cont

        self.player.update(self.keyMap, dt)

        self.tempEnemy.update(self.player, dt)

game = Game()
game.run()
