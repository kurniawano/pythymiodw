#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:38:29 2017

@author: root
"""

from pythymiodw import ThymioReal

robot=ThymioReal()
#robot.init_read()
robot.sleep(1)
print('move')
robot.wheels(100,100)
robot.sleep(5)
robot.wheels(0,100)
robot.sleep(4)
robot.wheels(100,100)
robot.sleep(5)
robot.wheels(100,0)
robot.sleep(4)
robot.wheels(100,100)
robot.sleep(5)
print('stop')
robot.wheels(0,0)
robot.quit()