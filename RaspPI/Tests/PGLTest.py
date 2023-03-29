import sys
sys.path.append('RaspPI')
from PGLJourney import PGLJourney

def callback ():
    print("Callback called!")


pgl_journey = PGLJourney(callback)
pgl_journey.enter_zone(0)



