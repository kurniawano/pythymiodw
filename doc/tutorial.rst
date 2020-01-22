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

The first line imports the necessary classes and definitions. The second line instantiates an object of ThymioSim to do a simulation using Python's turtle. On the other hand, if you wish to control the real physical robot, you should write::

	from pythymiodw import *
	robot = ThymioReal()

The second line instantiates an object of ThymioReal. This creates a connection to the physical robot using asebamedulla (D-Bus). 

Once this first step is done, you can access the actuators and the sensors of the robot. Please check the API for the available properties and methods to access this. For example, to move the robot forward for one second, you should write::

	robot.wheels(100,100)
	robot.sleep(1)
	robot.wheels(0,0)

The first line moves the wheels at speed 100. The maximum number you can set for the speed is 500, which correspond to about 20 cm/s. The second line put the robot to continue moving for one second. The third line stops the robot by giving speed 0 to both wheels.

To disconnect the robot and quit, simply type::

	robot.quit()

Your first program to move the robot for one second should look like the following::

	from pythymiodw import *
	robot = ThymioReal()
	robot.wheels(100,100)
	robot.sleep(1)
	robot.wheels(0,0)
	robot.quit()

------------------
State Machine Mode
------------------

State machine mode behaves differently from the Normal mode. In state machine mode, you need to specify the following:
- start_state
- get_next_values()

The following template shows you how to write in State Machine mode::

    from pythymiodw import *
	from pythymiodw import io
	from pythymiodw.sm import *
	from libdw import sm
	from boxworld import thymio_world

	class MySMClass(sm.SM):
	    start_state=None
	    def get_next_values(self, state, inp):
            # These two lines is to stop the robot
            # by pressing the backward button.
            # This only works when using the real robot.
            # It will not work in simulator.
            if inp.button_backward:
                return 'halt', io.Action(0, 0)
            #####################################

            # ground = inp.prox_ground.reflected
            # ground = inp.prox_ground.ambiant

            # ground = inp.prox_ground.delta
            try:
                left = ground[0]
                right = ground[1]
            except:
                left = -1
                right = -1
            # print(left,right)
            next_state = state
            return next_state, io.Action(fv=0.0, rv=0.1)

        #########################################
        # Don't modify the code below.
        # this is to stop the state machine using
        # inputs from the robot
        #########################################
        def done(self, state):
            if state == 'halt':
                return True
            else:
                return False
                
	MySM=MySMClass()

	############################

	m=ThymioSMSim(MySM, thymio_world, scale=2)
	try:
	    m.start()
	except KeyboardInterrupt:
	    m.stop()

The first five lines simply import the necessary modules. In state machine mode, we need to create a child class of SM which is defined in sm module. In this child class, we need to define what is the starting state by overriding the `start_state` attribute. Moreover, we need to override the `get_next_values` method. This method takes in the current state and the current input and returns two outputs: next state and the output of the state machine. When using pythymiodw, the output of the state machine is an `io.Action` object. The output must be initialized to a particular forward velocity (`fv`) and rotational velocity (`rv`). 

The `inp` argument in `get_next_values()` is an object as described in [Common API](common). This means that the line `inp.button_backward` reads the value whether the directional button backward is pressed. If it is, it will give 1, otherwise 0. On the other hand, `inp.prox_ground` returns the object for light detector facing the ground at the front of Thymio. This contains three values `ambiant`, `reflected`, and `delta`. The most useful is `delta` as it gives the difference between the ambiant and the reflected value. This can be used to detect the color of the ground under the sensor. Each of these returns a list of two elements, where the first element is the left value and the second element is the right value of the sensor.

To stop the robot, press the backward button at the top of Thymio. You can also write the state machine to stop the robot by setting the `next_state` to `halt`. 