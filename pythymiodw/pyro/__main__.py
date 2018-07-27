import Pyro4
from pythymiodw import ThymioSimMR

def run_pyro_daemon():
    try:
        with Pyro4.Daemon() as daemon:
            ns = Pyro4.locateNS()
            uri = daemon.register(ThymioSimMR)
            ns.register('pythymiodw.thymiosimmr', uri)
            daemon.requestLoop()
    except Exception as e:
        print(e)

run_pyro_daemon()