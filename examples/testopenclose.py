import sys
sys.path.append('..')

import pythymiodw as tdw
import time

tdw.open()
m=tdw.Thymio()
print 'launching'
time.sleep(1)
print 'closing'
tdw.close()

