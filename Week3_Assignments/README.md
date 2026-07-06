Documentation

ROS2 BASICS

QUESTION 1.

A basic approach to this problem was taken as there wasnt much else to do other than publish and subscribe.
I assumed that default values for the datas that are to be published.
Figuring out syntaxes was tough but gemini did a lot of help with it.
The video for the implementation is attached.
Photos for the cli part is attached.

QUESTION 2.

Defined a data type beforehand as was asked by the question and it was published by the publisher. Values change in a set manner to replicate a real rover (i presume).
A lot of dealing with terminal commands and going in and out of folders was new. But yeah gemini helped a lot.
Video is attached.

ROS2 TRANSFORMS & IKFK

QUESTION 1.

Photos attached.
It was simple. Most part of it was algebraic and a few set of formulas did all the work.

QUESTION 2.

First set up the inital postition somewhere in the reachable area(i took the one given in the example). Take input from the user regarding the which axis they want to move upon and how much. Use Inverse Kinematics to figure out the angles. Then publish it to move the robot in rviz to the desired location. Update the current location internally.

Couldnt fix the flicker problem that happens whenever i run the controller script.
Video is attached.
