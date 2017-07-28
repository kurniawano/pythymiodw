import sys
sys.path.append('..')
from pythymiodw import Thymio

m=Thymio()
m.init_read()
while(1):
    m.wheels(100,100)
    data=m.prox_sensors_val
    front=data[2]
    print front
    if front>3000:
	m.quit()
	break

