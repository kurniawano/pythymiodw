import dbus
import dbus.mainloop.glib
import gobject
import sys
import time
from optparse import OptionParser
 
proxSensorsVal=[0,0,0,0,0]

def dbusReply():
    pass

def dbusError(e):
    print 'error %s'
    print str(e)

def Braitenberg():
    #get the values of the sensors
    network.GetVariable("thymio-II", "prox.horizontal",reply_handler=get_variables_reply,error_handler=get_variables_error)
 
    #print the proximity sensors value in the terminal
    print proxSensorsVal[0],proxSensorsVal[1],proxSensorsVal[2],proxSensorsVal[3],proxSensorsVal[4]
 
    #send motor value to the robot
    #network.SetVariable("thymio-II", "motor.left.target", [-100])
    #network.SendEventName('SetColor', [32,0,32], reply_handler = dbusReply ,error_handler=dbusError)
    char = sys.stdin.read(1)
    if char == 'w':
       network.SendEventName('event1', [32,0,32,0,32,0,32,0], reply_handler = dbusReply ,error_handler=dbusError)
    if char == 'w':
       network.SetVariable("thymio-II", "motor.left.target", [300])
       network.SetVariable("thymio-II", "motor.right.target", [300])
       time.sleep(1) 
       network.SetVariable("thymio-II", "motor.left.target", [0])
       network.SetVariable("thymio-II", "motor.right.target", [0])
    if char == 's':
       network.SetVariable("thymio-II", "motor.left.target", [-300])
       network.SetVariable("thymio-II", "motor.right.target", [-300])
       time.sleep(1) 
       network.SetVariable("thymio-II", "motor.left.target", [0])
       network.SetVariable("thymio-II", "motor.right.target", [0])
    if char == 'a':
       network.SetVariable("thymio-II", "motor.left.target", [-300])
       network.SetVariable("thymio-II", "motor.right.target", [300])
       time.sleep(0.2) 
       network.SetVariable("thymio-II", "motor.left.target", [0])
       network.SetVariable("thymio-II", "motor.right.target", [0])
    if char == 'd':
       network.SetVariable("thymio-II", "motor.left.target", [300])
       network.SetVariable("thymio-II", "motor.right.target", [-300])
       time.sleep(0.2) 
       network.SetVariable("thymio-II", "motor.left.target", [0])
       network.SetVariable("thymio-II", "motor.right.target", [0])
    return True
 
def get_variables_reply(r):
    global proxSensorsVal
    proxSensorsVal=r
 
def get_variables_error(e):
    print 'error:'
    print str(e)
    loop.quit()
 
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
    (options, args) = parser.parse_args()
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()
 
    #Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
 
    #print in the terminal the name of each Aseba NOde
    print network.GetNodesList()  
    #GObject loop
    #print 'starting loop'
    loop = gobject.MainLoop()
    #call the callback of Braitenberg algorithm
    handle = gobject.timeout_add (100, Braitenberg) #every 0.1 sec
    loop.run()
