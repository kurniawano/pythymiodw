import sys
#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
m.init_read()
while(1):
    m.wheels(50,50)
    data=m.prox_horizontal
    front=data[2]
    print front
    if front>2000:
	m.quit()
	break
