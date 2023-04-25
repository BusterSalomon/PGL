# initialize timer object
from PGLJourney import PGLJourney
from PGLServerAPI import PGLServerAPI
from PGLModel import PGLZigbeeDevice, PGLModel

class PGLZoneController:
    
    def __init__(self, num_zones: int, devices_model: PGLModel = None):
        # Initialise attributes
        self.zones_devices_map: dict[int, dict[str, str]] = {}
        self.current_zone: int = None

        # If a devices model is given, then bind devices to zone in increasing order
        if devices_model:
            # Bind devices to zones
            for index, device in enumerate(devices_model.sensors_list):
                self.bind_device_to_zone(zone_id=index, device=device)
            for index, device in enumerate(devices_model.actuators_list):
                self.bind_device_to_zone(zone_id=index, device=device)

        # Set attributes
        self.zone_count = len(self.zones_devices_map)
        self.direction = "forward"
        self.server_api = PGLServerAPI("test.mosquitto.org")
        self.journey = PGLJourney(self.zone_count - 1, self.server_api.add_event_to_queue) # the last zone is the bathroom zone, needed in journey class 
                                                       # to know when bathroom is visited. We want the timer thread to be able to add event to the queue

    # Add device to {zone: device} map
    def bind_device_to_zone (self, zone_id: int, device: PGLZigbeeDevice) -> None:
        # zone_n: {"pir" : device_id,
        #          "led" : device id }
        if self.zones_devices_map.get(zone_id):
            self.zones_devices_map[zone_id][device.type_] = device.id_
        else:
            self.zones_devices_map[zone_id] = {device.type_: device.id_}
    
    # Get zone associated to device_id
    def get_zone_from_device_id (self, device_id: str) -> int:
        # Return -1 if not found
        zone_to_return = -1
        
        # Enumerate through devices map
        for _, zone in enumerate(self.zones_devices_map):
            #  Check if pir sensor in zone matches device_id if it exist
            if (self.zones_devices_map[zone].get("pir") 
                    and self.zones_devices_map[zone]["pir"] == device_id):
                 zone_to_return = zone
            
            #  Check if led in zone matches device_id if it exist
            elif (self.zones_devices_map[zone].get("led") 
                    and self.zones_devices_map[zone]["led"] == device_id):
                zone_to_return = zone
            
        # Return zone
        return zone_to_return

    # get_device_id_from_zone_id
    # Returns device_id of given type of zone
    def get_device_id_from_zone_id (self, zone_id: int, type: str) -> str:
        return self.zones_devices_map[zone_id][type]
    
    # get_device_ids_from_zone_ids
    # Returns a list of device ids of given types given a list of zone ids
    def get_device_ids_from_zone_ids (self, zone_ids: list[int], types: list[str]):
        device_ids = []
        for index, zone_id in enumerate(zone_ids):
            device_ids.append(self.zones_devices_map[zone_id][types[index]])
        return device_ids
    
    # get_zones_devices_map
    # Returns zone_devices_map
    def get_zones_devices_map (self) -> dict[int, dict[str, str]]:
        return self.zones_devices_map
    
    # Main control
    def control_zones(self, occupancy, device_id):
        if occupancy:
            zone = self.get_zone_from_device_id(device_id)
            if self.current_zone == None and zone == 0: # if the user enters the first zone
                self.journey.enter_zone(zone) # to do
            elif abs(zone - self.current_zone) == 1: # if the user enters the next zone
                self.journey.enter_zone(zone)
                if zone < self.current_zone: # if the user enters the previous zone
                    self.direction = "backwards"
                else:
                    self.direction = "forwards" # if the user enters the next zone
            else:
                pass # what happens if the user skips a zone?
            self.current_zone = zone
        # lights is a tuple of the current zone and the next zone, depending on the direction
        lights = (self.current_zone, 
                  self.current_zone + 1 if self.direction == "forwards" else self.current_zone - 1) 
        
        if self.journey.is_journey_complete():
            journey_str = self.journey.get_journey_to_string()
            self.server_api.add_event_to_queue(journey_str, "journey")
            self.journey.stop_worker.set()
            self.journey = PGLJourney(self.zone_count - 1, self.server_api.add_event_to_queue)
            self.current_zone = None
            self.direction = "forwards"
            return (self.journey.get_journey_to_string(), lights)
        
        return self.journey.get_journey_to_string(), lights
    
    
    