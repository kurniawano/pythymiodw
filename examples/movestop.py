import sys
#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
m.init_read()
while(1):
    m.wheels(100,100)
    data=m.prox_sensors_val
    front=data[2]
    print front
    if front>2000:
	m.quit()
	break

