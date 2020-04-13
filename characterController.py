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
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionTube

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        #loader.loadModel("Models/Misc/environment")
        self.environment = loader.loadModel("mirroredwalltest.x")
        self.environment.reparentTo(render)
        self.environment.getChild(0).setPos(0,50,-4)
        self.environment.getChild(0).setH(90)
        self.environment.getChild(0).setP(0)


        self.tempActor = Actor("shape-boi-grab-test-point_level2",
                                {"walk":"shape-boi-grab-test-point_level2-ArmatureAction",
                                 "lift":"shape-boi-grab-test-point_level2-IcosphereAction"})
        self.tempActor.reparentTo(render)
        self.tempActor.getChild(0).setH(180)
        self.tempActor.getChild(0).setPos(0,54,-4)
        self.tempActor.getChild(0).setScale(0.5,0.5,0.5)
        self.tempActor.loop("walk")

        self.tempActor2 = Actor("shape-boi-grab-test",{"walk":"shape-boi-grab-test-ArmatureAction"})
        self.tempActor2.reparentTo(render)
        self.tempActor2.getChild(0).setH(180)
        self.tempActor2.getChild(0).setPos(0,50,0)
        self.tempActor2.getChild(0).setScale(0.5,0.5,0.5)
        self.tempActor2.loop("walk")


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


        #player 1
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        colliderNode = CollisionNode("player")
        # Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
        colliderNode.addSolid(CollisionSphere(0, 54, -4, 1.3))
        collider = self.tempActor.attachNewNode(colliderNode)
        #collider.show()
        base.pusher.addCollider(collider, self.tempActor)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher)
        self.pusher.setHorizontal(True)

        #player 2
        self.cTrav2 = CollisionTraverser()
        self.pusher2 = CollisionHandlerPusher()
        colliderNode = CollisionNode("player")
        # Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
        colliderNode.addSolid(CollisionSphere(0, 50, 0, 1.3))
        collider = self.tempActor2.attachNewNode(colliderNode)
        #collider.show()
        base.pusher.addCollider(collider, self.tempActor2)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        base.cTrav.addCollider(collider, self.pusher2)
        self.pusher2.setHorizontal(True)

        # walls
        wallSolid = CollisionTube(-10.0, 32, -2, 10, 32, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-10.0, 51, -2, 10, 51, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(-8.0, 30, -2, -8, 55, -2, 1.2)
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)
        wall.setY(8.0)
        wall.show()

        wallSolid = CollisionTube(8.0, 30, -2, 8, 55, -2, 1.2)
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

    def selectionLight(self, selection):
        vectorToObject = selection.getPos()-self.tempActor.getPos()
        vector2d = vectorToObject.getXy()
        distanceToObject = vector2d.length()
        ambient = AmbientLight('ambient')
        ambient.setColor((0.5, 0.75, 0.5, 1))
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
        vectorToObject = self.tempActor2.getPos()-self.tempActor.getPos()
        vector2d = vectorToObject.getXy()
        distanceToObject = vector2d.length()

        if distanceToObject < 0.6:
            print(distanceToObject, "pickup")
            #self.selectionLight(self.tempActor2)
            self.tempActor2.setX(self.tempActor.getX() + 0.25)
            self.tempActor2.setY(self.tempActor.getY() + 0.25)
            self.tempActor2.setZ(self.tempActor.getZ() + 0.25)

    def setObjectDown(self):
        #self.tempActor2.setX(self.tempActor2.getX() + 0.25)
        #self.tempActor2.setY(self.tempActor2.getY() + 0.25)
        self.tempActor2.setZ(-4)
    def cameraFollow(self):
        base.disableMouse()
        self.camera.setPos(self.tempActor.getPos()+ Vec3(0,12,4))
        self.camera.setP(-12.5)
    def cameraSet(self):
        base.disableMouse()
        self.camera.setPos(0, 0, 50)
        # Tilt the camera down by setting its pitch.
        self.camera.setP(-45)


    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print (controlName, "set to", controlState)
    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        self.selectionLight(self.tempActor2)

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
