import Pyro4
from pythymiodw import ThymioSim3D

def run_pyro_daemon():
    try:
        with Pyro4.Daemon() as daemon:
            ns = Pyro4.locateNS()
            uri = daemon.register(ThymioSim3D)
            ns.register('pythymiodw.thymiosim3d', uri)
            daemon.requestLoop()
    except Exception as e:
        print(e)

run_pyro_daemon()