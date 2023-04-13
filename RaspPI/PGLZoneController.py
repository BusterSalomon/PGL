# initialize timer object
from PGLJourney import PGLJourney
from PGLServerAPI import PGLServerAPI

class PGLZoneController:
    
    def __init__(self, devices):
        self.devices = devices
        self.zones = {}
        self.current_zone = None
        for i, device in enumerate(devices):
            if device.type_ == "pir":
                self.zones[device.id_] = i
        self.zone_count = len(self.zones)
        self.journey = PGLJourney(self.zone_count - 1) # the last zone is the bathroom zone, needed in journey class 
                                                       # to know when bathroom is visited.
        self.direction = "forward"
        self.server_api = PGLServerAPI("localhost")


    def control_zones(self, occupancy, device_id):
        if occupancy:
            zone = self.zones[device_id]
            if self.current_zone == None and zone == 0: # if the user enters the first zone
                self.current_zone = zone
                self.journey.enter_zone(zone) # to do
            elif zone + 1 == self.current_zone or zone - 1 == self.current_zone: # if the user enters the next zone
                self.current_zone = zone
                self.journey.enter_zone(zone)
                if zone < self.current_zone: # if the user enters the previous zone
                    self.direction = "backwards"
                else:
                    self.direction = "forwards" # if the user enters the next zone
            else:
                pass # what happens if the user skips a zone?
        # lights is a tuple of the current zone and the next zone, depending on the direction
        lights = (self.current_zone, 
                  self.current_zone + 1 if self.direction == "forwards" else self.current_zone - 1) 
        
        if self.journey.is_journey_complete():
            journey_str = self.journey.get_journey_to_string()
            self.server_api.post_journey(journey_str)
            self.journey = PGLJourney(self.zone_count - 1)
            self.current_zone = None
            self.direction = "forwards"
            return self.journey.get_zones(), lights
        
        return self.journey.get_zones(), lights
    
    
    