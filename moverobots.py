from pythymiodw import *
import time


m=Thymio()
m.wheels(300,300)
time.sleep(1)
m.wheels(-300,300)
time.sleep(1)
m.wheels(300,-300)
time.sleep(1)
m.halt()

