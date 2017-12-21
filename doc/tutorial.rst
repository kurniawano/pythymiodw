================
Tutorials
================

------------
Introduction
------------

The library PyThymioDW allows you to run a simulation using Python's turtle module as well as controlling the physical Thymio robot. For both, you can write your program in two modes: the normal mode and the state machine mode.

-----------
Normal Mode
-----------
To run in normal mode, you need either to import ThymioReal or ThymioSim class, depending on whether you want to control the real physical robot, or just doing a simulation using Python's turtle. For example, to do create a simulation, you should write::

	from pythymiodw import *
	robot = ThymioSim()
	robot.init_read()

The first line imports the necessary classes and definitions. The second line instantiates an object of ThymioSim to do a simulation using Python's turtle. The third line initiates simulation for reading sensor data. On the other hand, if you wish to control the real physical robot, you should write::

	from pythymiodw import *
	robot = ThymioReal()
	robot.init_read()

The second line instantiates an object of ThymioReal. This creates a connection to the physical robot using asebamedulla (D-Bus). The third line initiates the sensor readings of the physical robot.

Once this first step is done, you can access the actuators and the sensors of the robot. Please check the API for the available properties and methods to access this. For example, to move the robot forward for one second, you should write::

	robot.wheels(100,100)
	robot.sleep(1)
	robot.wheels(0,0)

The first line moves the wheels at speed 100. The maximum number you can set for the speed is 500, which correspond to about 20 cm/s. The second line put the robot to continue moving for one second. The third line stops the robot by giving speed 0 to both wheels.

To disconnect the robot and quit, simply type::

	robot.quit()

Your first program to move the robot for one second should looks like the following::

	from pythymiodw import *
	robot = ThymioReal()
	robot.init_read()
	robot.wheels(100,100)
	robot.sleep(1)
	robot.wheels(0,0)
	robot.quit()

------------------
State Machine Mode
------------------
