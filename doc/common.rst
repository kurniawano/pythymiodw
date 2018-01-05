===================================================
Commonly Used Methods and Properties in Normal Mode
===================================================

-----
Setup
-----

* ``ThymioReal()``
	This is used to instantiate an object to control the real physical robot.

* ``ThymioSim(world=None)``
	This is used to instantiate an object to control a simulation using Python's turtle module. You can provide the world for the simulator to draw.  The world must be of the type ``World`` from ``pythymio.world``. 


---------
Actuators
---------

* ``obj.wheels(ls, rs)``
	Set the left and right wheels' speed. The value ranges from -500 to 500. A negative value means the wheels will rotate on the opposite direction. This can be used to move backward or to turn. A speed of 500 on both wheels will move the robot forward at about 20 cm/s. This method does not return anything.

* ``obj.leds_top(r=0, g=0, b=0)``: Sets the intensity of the top RGB led.

* ``obj.leds_circle(led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0)``: where led0 sets the intensity of the LED at the front of the robot, the others are numbered clockwise.

* ``obj.leds_buttons(led0=0, led1=0, led2=0, led3=0)``:

* ``obj.leds_prox_h(led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0)``: Sets the LEDs of the front and back proximity sensors. led0 to led5 correspond to front LED from left to right, while led6 and led7 correspond to the back LED left and right. 

* ``obj.leds_prox_v(led0=0, led1=0, led2=0, led3=0, led4=0, led5=0, led6=0, led7=0)`` : Sets the LEDs associated with the bottom sensors, left and right.

--------
Sensors
--------

* ``obj.prox_horizontal`` 
	Returns the horizontal proximity sensors as a list of six integers. A non-zero value means there is an obstacle detected. The closer the obstacle is to the robot, the higher the values of these sensors be. 

	* index 0: front left
	* index 1: front middle-left
	* index 2: front centre
	* index 3: front middle-right
	* index 4: front right
	* index 5: back left
	* index 5: back right

* ``obj.prox_ground``
	Returns an io.ProxGround object which contains the following attributes:

	* ``delta``: difference between reflected light and ambient light, linked to the distance and to the ground colour.
	* ``reflected``: amount of light received when the sensor emits infrared, varies between 0 (no reflected light) and 1023 (maximum reflected light).
	* ``ambiant``: ambient light intensity at the ground, varies between 0 (no light) and 1023 (maximum light).
	
	For each array, index 0 refers to the left sensor, and index 1 refers to the right sensor. 

* ``obj.temperature``
	Returns the temperature in Celcius. The returned value is a float.

* ``obj.accelerometer``
	Returns a tuple of three elements which are the x, y, and z acceleration from the acelerometer.

* ``obj.button_forward``
	Returns 1 if the forward button is pressed, 0 otherwise.

* ``obj.button_backward``
	Returns 1 if the backward button is pressed, 0 otherwise.

* ``obj.button_center``
	Returns 1 if the center button is pressed, 0 otherwise.

* ``obj.button_left``
	Returns 1 if the left button is pressed, 0 otherwise.

* ``obj.button_right``
	Returns 1 if the right button is pressed, 0 otherwise.
