###############################################################################
# Name: Morgan Visnesky
# AndewID: mvisnesk
# FileName: bulletPhysicsTest.py
###############################################################################
'''
    - Trial run using alternate physics option built into panda3D
    - Trial run instancing objects and materials in a for loop
'''
# CITATIONS:
# https://docs.panda3d.org/1.10/python/programming/physics/bullet/hello-world
# https://docs.panda3d.org/1.10/python/programming/scene-graph/instancing
# https://docs.panda3d.org/1.10/python/programming/physics/bullet/debug-renderer
# ^^ debug renderer is super useful ^^
# https://discourse.panda3d.org/t/picker-class-for-panda3d-objects/15831
# ^^ picker class ^^

import direct.directbase.DirectStart
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import *
from direct.actor.Actor import Actor
from panda3d.bullet import BulletDebugNode
from panda3d.physics import *
debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()

base.cam.setPos(20, -100, 40)
base.cam.lookAt(0, 0, 0)







'''
Picker class for Panda3d.

Created on Oct 31, 2017

@author: consultit
'''

from panda3d.core import CollisionTraverser, CollisionHandlerQueue, CollisionNode, CollisionRay, \
    BitMask32, LPoint3f, NodePath, CardMaker
from direct.showbase.ShowBase import ShowBase

class Picker(object):
    '''
    A class for picking (Panda3d) objects.
    '''

    def __init__(self, app, render, camera, mouseWatcher, pickKeyOn, pickKeyOff, collideMask,
                 pickableTag="pickable"):
        self.render = render
        self.mouseWatcher = mouseWatcher.node()
        self.camera = camera
        self.camLens = camera.node().get_lens()
        self.collideMask = collideMask
        self.pickableTag = pickableTag
        self.taskMgr = app.task_mgr
        # setup event callback for picking body
        self.pickKeyOn = pickKeyOn
        self.pickKeyOff = pickKeyOff
        app.accept(self.pickKeyOn, self._pickBody, [self.pickKeyOn])
        app.accept(self.pickKeyOff, self._pickBody, [self.pickKeyOff])
        # collision data
        self.collideMask = collideMask
        self.cTrav = CollisionTraverser()
        self.collisionHandler = CollisionHandlerQueue()
        self.pickerRay = CollisionRay()
        pickerNode = CollisionNode("Utilities.pickerNode")
        node = NodePath("PhysicsNode")
        node.reparentTo(render)
        anp = node.attachNewNode(pickerNode)
        base.physicsMgr.attachPhysicalNode(pickerNode)
        pickerNode.add_solid(self.pickerRay)
        pickerNode.set_from_collide_mask(self.collideMask)
        pickerNode.set_into_collide_mask(BitMask32.all_off())
        #pickerNode.node().getPhysicsObject().setMass(10)
        self.cTrav.add_collider(self.render.attach_new_node(pickerNode), self.collisionHandler)
        # service data
        self.pickedBody = None
        self.oldPickingDist = 0.0
        self.deltaDist = 0.0
        self.dragging = False
        self.updateTask = None

    def _pickBody(self, event):
        # handle body picking
        if event == self.pickKeyOn:
            # check mouse position
            if self.mouseWatcher.has_mouse():
                # Get to and from pos in camera coordinates
                pMouse = self.mouseWatcher.get_mouse()
                #
                pFrom = LPoint3f()
                pTo = LPoint3f()
                if self.camLens.extrude(pMouse, pFrom, pTo):
                    # Transform to global coordinates
                    rayFromWorld = self.render.get_relative_point(self.camera, pFrom)
                    rayToWorld = self.render.get_relative_point(self.camera, pTo)
                    # cast a ray to detect a body
                    # traverse downward starting at rayOrigin
                    self.pickerRay.set_direction(rayToWorld - rayFromWorld)
                    self.pickerRay.set_origin(rayFromWorld)
                    self.cTrav.traverse(self.render)
                    if self.collisionHandler.get_num_entries() > 0:
                        self.collisionHandler.sort_entries()
                        entry0 = self.collisionHandler.get_entry(0)
                        hitPos = entry0.get_surface_point(self.render)
                        # get the first parent with name
                        pickedObject = entry0.get_into_node_path()
                        while not pickedObject.has_tag(self.pickableTag):
                            pickedObject = pickedObject.getParent()
                            if not pickedObject:
                                return
                            if pickedObject == self.render:
                                return
                        #
                        self.pickedBody = pickedObject

                        self.oldPickingDist = (hitPos - rayFromWorld).length()
                        self.deltaDist = (self.pickedBody.get_pos(self.render) - hitPos)
                        print(self.pickedBody.get_name(), hitPos)
                        if not self.dragging:
                            self.dragging = True
                            # create the task for updating picked body motion
                            self.updateTask = self.taskMgr.add(self._movePickedBody,
                                                                    "_movePickedBody")
                            # set sort/priority
                            self.updateTask.set_sort(0)
                            self.updateTask.set_priority(0)
        else:

            if self.dragging:
                # remove pick body motion update task
                self.taskMgr.remove("_movePickedBody")
                self.updateTask = None
                self.dragging = False
                self.pickedBody = None



    def _movePickedBody(self, task):
        # handle picked body if any
        if self.pickedBody and self.dragging:
            # check mouse position
            if self.mouseWatcher.has_mouse():
                # Get to and from pos in camera coordinates
                pMouse = self.mouseWatcher.get_mouse()
                #
                pFrom = LPoint3f()
                pTo = LPoint3f()
                if self.camLens.extrude(pMouse, pFrom, pTo):
                    # Transform to global coordinates
                    rayFromWorld = self.render.get_relative_point(self.camera, pFrom)
                    rayToWorld = self.render.get_relative_point(self.camera, pTo)
                    # keep it at the same picking distance
                    direction = (rayToWorld - rayFromWorld).normalized()
                    direction *= self.oldPickingDist
                    self.pickedBody.set_pos(self.render, rayFromWorld + direction + self.deltaDist)
                    #self.pickedBody.reparentTo(np)
                    #self.pickedBody.setMass(10.0)

        #
        return task.cont


PICKABLETAG = "pickable"
PICKKEYON = "mouse3"
PICKKEYOFF = "mouse3-up"
#picker = Picker(base, base.render, base.cam, base.mouseWatcher, PICKKEYON, PICKKEYOFF,
                #BitMask32.all_on(), PICKABLETAG)
# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))
#world.setDebugNode(debugNP.node())
for i in range(50):
    '''
    shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
    node = BulletRigidBodyNode('Ground')
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, 0, -2)
    world.attachRigidBody(node)
    '''
    # Box
    shape = BulletBoxShape(Vec3(1.5, 0.75, 0.5))
    node = BulletRigidBodyNode('Box')
    node.setMass(10.0)
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, 0, (i*5)+15)
    world.attachRigidBody(node)
    model = loader.loadModel('models/isospherebaby2.x')
    model.setScale(0.5,0.5,0.25)
    #model.flattenLight()
    model.reparentTo(np)
    model.set_tag(PICKABLETAG, "")

# lights coppied from pandas3dTest.py file
# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
world.attachRigidBody(node)
model = loader.loadModel('mirroredwalltest.x')
model.setPos(0,0,-1.5)
model.setScale(4,4,4)
model.setHpr(90, -270, 0)
model.reparentTo(np)

shape = BulletBoxShape(Vec3(0.5, 50, 10))
node = BulletRigidBodyNode('Wall')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(-30, 0, 5)
world.attachRigidBody(node)

shape = BulletBoxShape(Vec3(0.5, 50, 10))
node = BulletRigidBodyNode('Wall')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(30, 0, 5)
world.attachRigidBody(node)

shape = BulletBoxShape(Vec3(0.5, 35, 10))
node = BulletRigidBodyNode('Wall')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(-10, -38, 5)
np.setHpr(90,0,0)
world.attachRigidBody(node)

shape = BulletBoxShape(Vec3(1.5, 2.5, 100))
node = BulletRigidBodyNode('Tower')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(-5, -20, 5)
np.setHpr(90,0,0)
world.attachRigidBody(node)

shape = BulletBoxShape(Vec3(1, 2, 100))
node = BulletRigidBodyNode('Tower')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(-18, 24, 5)
np.setHpr(90,0,0)
world.attachRigidBody(node)

# Box
shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
node = BulletRigidBodyNode('Box')
node.setMass(1.0)
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, 15)
world.attachRigidBody(node)
model = loader.loadModel('models/isospherebaby2.x')
model.setScale(0.5,0.5,0.5)
#model.flattenLight()
model.reparentTo(np)

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

'''
dancer = loader.loadModel('models/isospherebaby2.x')
#dancer.loop("kick")
#dancer.setPos(0,0,0)
dancer.setScale(0.5,0.5,0.5)
for i in range(50):
    placeholder = render.attachNewNode("Dancer-Placeholder")
    placeholder.setPos(i*10, i*20, i*50)
    dancer.instanceTo(placeholder)
'''



# Update
def update(task):
    dt = globalClock.getDt()
    world.doPhysics(dt)

    return task.cont


base.disable_mouse()
taskMgr.add(update, 'update')
base.run()
