import time

class Journey:
    
    def __init__(self, zones) -> None:
        self.zones = zones
        self.entered_zones = []

    def enter_zone(self, zone):
        self.entered_zones.append(zone)
        print(self.entered_zones)
    
    def get_zones(self):
        return self.entered_zones


















