
#shape-boi.py
## A CMU 15-112 Term Project (Spring 2020)

##### **shape-boi.  a shape in a world, looking for fun, and friendship.**

Shape-boi aims to be an interactive VR-like social experience.  Built using python versions of panda3D and openCV, this app allows you to interact with twitter in a unique 3D game space.

##Features:
* **Cool 3D game engine:** Using panda3D and one of its built-in physics options, Bullet Physics Engine, shape-boi achieves interesting physics interactions, and hosts aesthetically appealing content created in blender.

* **Color tracking with openCV:** Moves shape-boi around their 3D world, and eventually should allow users to pick up and interact with 3D game objects.

* **Twitter API:** Connects to a given user account and ultimately gives user control over all of its functions, mainly the ability to view most recent tweets represented by game objects and game UI.

* **Shape playground:** Allows you to instance a number of shapes, to build with, toss around the play room, or toss through a portal.  Wait what? A portal? Read on...

* **Portals:** Hopefully... portals will be implemented into shape-boi's world.  A portal would allow you to pass from one room to another, possibly enter new levels, or change shape-boi's shape.

# Working Functionality
* Color tracking (currently set to golden yellow color).
* UDP sockets to listen for (x,y) of center of tracked object.
* Custom game objects that move / respond to incoming UDP events.
* Game physics (not tied into driver file at the moment)

#Getting started(current version):
- Need python3
- Need panda3D
- Need openCV
- Put included models in default panda3D models directory

#### Once started:
- In a terminal window navigate to the directory holding shape-boi's files and run `python3 pandas3DTest.py`

- Click 'Open Connection' button to start UDP server, it will print 'UDP server up and listening' when it has connected.

- After a connection has been made, click 'Color Track', which will enable the functionality to control shape-boi with a yellow colored object.

- To exit the application, hit 'CTRL-C' in the interpreter you ran the pandas3DTest.py file from

# TODO as of 04/09/2020:
* Re-structure code to make more organized.
* Document code more thoroughly.
* Build and export final game objects using blender. - progress being made 04/13/2020
* Write classes to handle connecting to and managing twitter API calls.
* Get working GLSL for portals.
* Program portal functionality
* Finger tracking for grabbing and moving game objects.
* Working on different 'levels' / environments.
* Finalize UI overlay and pack into a class or function.
* Bind object to movement function instead of incoming UDP (x,y) values. - working 04/13/2020
* Collision detection. - working 04/13/2020
* Exit openCV when closing app.
* Turn UDP handler into its own class.


# NOTES
* https://github.com/09th/YABEE/blob/master/YABEE_HowTo.pdf
* https://www.youtube.com/playlist?list=PLcMfSPR_1EGipilDrE2AfIYG36JCwwM1l
* mapping scale from blender to panda3D should be one to one
