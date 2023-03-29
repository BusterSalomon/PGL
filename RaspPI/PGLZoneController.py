from PGLJourney import PGLJourney
from PGLZigbee2mqttClient import PGLZigbee2mqttMessage

class PGLZoneController:

    # CONSTRUCTOR
    def __init__(self):
        # Initiate refference to pgl_journey
        self.pgl_journey = PGLJourney()

        # Inititate active lights to off
        self.active_lights = [False, False, False, False, False]
    
    # METHODS
    def control_zones(self, occupancy: bool, device_id: str):        
        
        self.pgl_joruney = PGLJourney()

        pass
    
    

# controlZones method takes message data (json) and sensor ID