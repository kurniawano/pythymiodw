from pythymiodw.pyro import Thymio3D
import time

thymio = Thymio3D()
print('Changing wheel speed.')
thymio.wheels(100, 101)
print('Now run C# project to change prox_horizontal and prox_ground.')
print('You have 15 sec before this code starts to read.')
time.sleep(15)
print(thymio.prox_horizontal)
pg = thymio.prox_ground
print(pg.delta, pg.ambiant, pg.reflected)
thymio.quit()
