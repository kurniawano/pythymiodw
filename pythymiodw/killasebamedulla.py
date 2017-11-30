import os
import signal
pids=[pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    try:
        process=open(os.path.join('/proc',pid,'cmdline'),'rb').read()
        process=str(process,'utf-8')
        if ('asebamedulla' in process):
            pid=int(pid)
            os.kill(pid,signal.SIGTERM)
            print('Kill asebamedulla.')
    except IOError:
        continue
