import sys
#sys.path.append('..')
from pythymiodw import ThymioReal

m=ThymioReal()
while(1):
    m.wheels(50,50)
    data=m.prox_horizontal
    print(data)
    front=data[2]
    print(front)
    m.sleep(1)
    if front>2000:
        m.quit()
   

