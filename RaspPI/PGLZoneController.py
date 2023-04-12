# initialize timer object
from PGLJourney import PGLJourney

class PGLZoneController:
    
    def __init__(self, devices):
        self.devices = devices
        self.zones = {}
        self.current_zone = None
        for i, device in enumerate(devices):
            if device.type_ == "pir":
                self.zones[device.id_] = i
        self.zone_count = len(self.zones)
        self.journey = PGLJourney(self.zones)
        self.direction = "forward"

    def control_zones(self, occupancy, device_id):
        if occupancy:
            zone = self.zones[device_id]
            if self.current_zone == None and zone == 0: # if the user enters the first zone
                self.current_zone = zone
                self.journey.enter_zone(zone)
            elif zone + 1 == self.current_zone or zone - 1 == self.current_zone: # if the user enters the next zone
                self.current_zone = zone
                self.journey.enter_zone(zone)
                if zone < self.current_zone: # if the user enters the previous zone
                    self.direction = "backward"
                else:
                    self.direction = "forward" # if the user enters the next zone
            else:
                pass # what happens if the user skips a zone?
        # lights is a tuple of the current zone and the next zone, depending on the direction
        lights = (self.current_zone, 
                  self.current_zone + 1 if self.direction == "forward" else self.current_zone - 1) 
        return self.journey.get_zones(), lights

        

            
                
                

           
                

                    
                




# controlZones method takes message data (json) and sensor ID