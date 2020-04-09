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

import direct.directbase.DirectStart
from panda3d.core import Vec3
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.core import *
from direct.actor.Actor import Actor

base.cam.setPos(0, -30, 0)
base.cam.lookAt(0, 0, 0)

# World
world = BulletWorld()
world.setGravity(Vec3(0, 0, -9.81))

for i in range(50):
    shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
    node = BulletRigidBodyNode('Ground')
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, 0, -2)
    world.attachRigidBody(node)

    # Box
    shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
    node = BulletRigidBodyNode('Box')
    node.setMass(1.0)
    node.addShape(shape)
    np = render.attachNewNode(node)
    np.setPos(0, 0, (i*5)+15)
    world.attachRigidBody(node)
    model = loader.loadModel('models/isospherebaby2.x')
    model.setScale(0.5,0.5,0.25)
    #model.flattenLight()
    model.reparentTo(np)

# lights coppied from pandas3dTest.py file
# Plane
shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
node = BulletRigidBodyNode('Ground')
node.addShape(shape)
np = render.attachNewNode(node)
np.setPos(0, 0, -2)
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

taskMgr.add(update, 'update')
base.run()
