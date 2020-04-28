
#shape-boi
## A CMU 15-112 Term Project (Spring 2020)

##### **shape-boi.  a shape in a world, trying to save his loved ones.**

Shape-boi aims to be a fun VR-like gaming experience.  Built using Python versions of panda3D and openCV, this app allows you to control game characters with object tracking via your webcam.

##Features:
* Utilizes many features of the panda3D game engine for Python and C++.

* Use of openCV which allows for control of a players character with a yellow color tracked object.

* Game map, environment models, and character models, made with Blender.

* Game music made with ableton live.

* Game.py uses the subprocess module to run colorTrack.py, and uses sockets to listen to control messages being sent from the color tracker.

#Requirements:
- Python3
- Panda3D
- openCV

#### Getting started:
- In a terminal window navigate to the directory holding shape-boi's files and run `python3 Game.py`

- Click on the instructions button to view the instructions screen.  This has an overview of the game controls and how to enable the color tracking option.

- You may select the color track mode from the home menu before beginning the game.  If selected a tracking screen will pop up to help with your control.  To use this mode the controls are as follows: moving the color tracked object up will move the player forward, moving it down will move the player backward, right moves the player right, left moves the player left, and holding the object in the center of the track screen or removing it from view will cause the player to stand still.

- The default key controls are as follows: w - up, s - down, a - left, d - right.

- After deciding whether or not to use object tracking, clicking the start game button will take you to a character selection screen where you will have the option to choose between a handful of different characters to play the game with.

- From the character selection screen click the start game button which take you to the game, and begin the countdown timer.

- Your objective is to navigate around the game map, find shape-boi's friends and loved ones, and then carry them to the safe zone, where they can feel better.

- To lift up and carry a friend to the rescue zone you must be within close range of the friend.  When within range, the friend will become highlighted in a light golden yellow color.  Lift your friend by pressing the space bar, and hold it down to carry them.

- The 'p' key can be used to change between an overhead camera view, and a third person camera view.

- Your score is listed in the upper left corner of the game window, and the remaining time centered at the top of the window.

- If the game has been won, a message will be displayed along with 'Quit' and 'Play Again' buttons.

- If the game is lost, the screen will be tinted red, and a message will be displayed with the number of sad friends that were unable to be rescued.  A 'Quit' and 'Play Again' button are also shown on this screen.


#### Special Thanks
- Ian Eborn for his [tutorial](https://arsthaumaturgis.github.io/Panda3DTutorial.io/) for beginning game developers, and furthermore his thoughtful insight on panda3D's discourse page.
- All other members of panda3D discourse page for their help and past contributions.
- GrimFang's 'Panda3D Game Development' an excellent resource for anyone interested in creating games and other tools with python and Panda3D.



# Other resources
* https://github.com/09th/YABEE/blob/master/YABEE_HowTo.pdf
* https://www.youtube.com/playlist?list=PLcMfSPR_1EGipilDrE2AfIYG36JCwwM1l
