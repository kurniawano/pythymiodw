from pythymiodw.pyro import ThymioMR
import time

thymio = ThymioMR()
print('Changing wheel speed.')
thymio.wheels(100,101)
time.sleep(10)
print(thymio.prox_horizontal)
pg = thymio.prox_ground
print(pg.delta, pg.ambiant, pg.reflected)
thymio.quit()


