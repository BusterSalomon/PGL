from typing import Optional
from PGLJourney import PGLJourney
from PGLServerAPI import PGLServerAPI
from PGLModel import PGLZigbeeDevice, PGLModel

class PGLZoneController:
    """ Class that controls the zones of the house. 
    It is responsible for binding devices to zones, and for keeping track of the current zone.
    It is also responsible for keeping track of the led states of the devices. 
    It is responsible for passing events to server api.
    """
    def __init__(self, devices_model: PGLModel = None):
        # Initialise attributes
        self.zones_devices_map: dict[int, dict[str, str]] = {}
        self.led_states: dict[str, str] = {} # {device_id, state}
        self.current_zone: int = None

        # If a devices model is given, then bind devices to zone in increasing order
        # And initialise led states to off
        if devices_model:
            # Bind devices to zones
            for index, device in enumerate(devices_model.sensors_list):
                self.bind_device_to_zone(zone_id=index+1, device=device)
            for index, device in enumerate(devices_model.actuators_list):
                self.bind_device_to_zone(zone_id=index+1, device=device)
                self.led_states[device.id_] = "OFF" # Initialise led states to off

        # Set attributes
        self.zone_count = len(self.zones_devices_map)
        self.direction = "forwards"
        self.server_api = PGLServerAPI("test.mosquitto.org")
        self.journey = PGLJourney(self.zone_count, self.server_api.add_event_to_queue)
        # the last zone is the bathroom zone, needed in journey class
        # to know when bathroom is visited.
        # We want the timer thread to be able to add event to the queue


    def bind_device_to_zone (self, zone_id: int, device: PGLZigbeeDevice) -> None:
        """ Add device to {zone: device} map

        zone_n: {"pir" : device_id,
                 "led" : device id }"""
        if self.zones_devices_map.get(zone_id):
            self.zones_devices_map[zone_id][device.type_] = device.id_
        else:
            self.zones_devices_map[zone_id] = {device.type_: device.id_}


    def get_zone_from_device_id (self, device_id: str) -> int:
        """ Returns zone of given device_id """
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


    def get_device_id_from_zone_id (self, zone_id: int, device_type: str) -> str:
        """ Returns device_id of given type from given zone_id"""
        return self.zones_devices_map[zone_id][device_type]

    def get_device_ids_from_zone_ids (self, zone_ids: list[int], types: list[str]):
        """ Returns a list of device ids of given types given a list of zone ids"""
        device_ids = []
        for index, zone_id in enumerate(zone_ids):
            device_ids.append(self.zones_devices_map[zone_id][types[index]])
        return device_ids

    def get_zones_devices_map (self) -> dict[int, dict[str, str]]:
        """ Returns zone_devices_map"""
        return self.zones_devices_map

    
    # set_device_led_states
    # sets dictionary 
    def set_device_led_states (self, zone_to_turn_on: Optional[tuple[int, int]], turn_all_off : Optional[bool] = False):

        if turn_all_off == True:
            for _, cur_led_id in enumerate(self.led_states):
                self.led_states[cur_led_id] = "OFF"
            return None
        
        if zone_to_turn_on == None:
            return None    
        
        led_ids: list[str] = self.get_device_ids_from_zone_ids(list(zone_to_turn_on), types=["led", "led"])
        
        # Update all states
        for _, cur_led_id in enumerate(self.led_states):
            if (cur_led_id == led_ids[0] or cur_led_id == led_ids[1]):
                self.led_states[cur_led_id] = "ON"
            else:
                self.led_states[cur_led_id] = "OFF"

    def control_zones(self, device_id) -> Optional[dict[str, str]]:
        """ Main control function. 
        
        Takes in device_id of activated pir sensor.
        updates the journey object and returns led_states dictionary
        """
        # Update journey, and return true if zone is valid
        success : bool = self.__update_journey_zone(self.get_zone_from_device_id(device_id))
        if not success:
            self.set_device_led_states(None, turn_all_off=True)
            return self.led_states
        
        # lights is a tuple of the current zone and the next zone, depending on the direction
        zones_to_light_up = self.__get_zones_to_light_up()

        # Update led state dictionary
        self.set_device_led_states(zones_to_light_up)

        if self.journey.is_journey_complete():
            print("Journey is complete")
            self.__reset_and_send_journey()

        return self.led_states

    def __update_journey_zone(self, zone) -> bool:
        """ Updates the journey object with the given zone"""
        if self.current_zone is None and zone == 1: # if the user enters the first zone
            self.journey.enter_zone(zone)

        elif self.current_zone == None:     #if user enters random zone without being in any previously
            return False
        
        elif abs(zone - self.current_zone) <= 1: # if the user enters the next zone or stays in the current
            self.journey.enter_zone(zone)
            if zone < self.current_zone: # if the user enters the previous zone
                self.direction = "backwards"
            else:
                self.direction = "forwards" # if the user enters the next zone
        else:
        # if the user enters a zone that is not the next or previous zone,
        # current zone is not updated
            return False
        self.current_zone = zone
        return True

    def __get_zones_to_light_up(self) -> Optional[tuple[int, int]]:
        """ Returns a tuple of the current zone and the next zone, depending on the direction"""
        if self.current_zone is None:
            return None
        if self.direction == "forwards" and self.current_zone + 1 <= self.zone_count:       #going forward and zones left
            zones_to_light_up = (self.current_zone, self.current_zone + 1)
        elif self.direction == "backwards" and self.current_zone - 1 > 0:                   #going backwards and zones left
            zones_to_light_up = (self.current_zone, self.current_zone - 1)
        elif self.direction == "backwards" and self.current_zone == 1:                      #reached the bedroom
            zones_to_light_up = (self.current_zone, self.current_zone)
        elif self.direction == "forwards" and self.current_zone == self.zone_count:         #reached the bathroom
            zones_to_light_up = (self.current_zone-1, self.current_zone)
        else:                                                                               #in the same zone as before in the middle of the route
            zones_to_light_up = (self.current_zone - 1, self.current_zone)
        return zones_to_light_up

    # Resets the journey and sends the journey to the server
    def __reset_and_send_journey(self) -> None:
        """ Resets the journey and sends the journey to the server"""
        journey_str = self.journey.get_journey_to_string()
        self.server_api.add_event_to_queue(journey_str, "journey")
        self.journey.stop_worker.set()
        self.journey = PGLJourney(self.zone_count, self.server_api.add_event_to_queue)
        self.current_zone = None
        self.direction = "forwards"
