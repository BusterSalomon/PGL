# Imports
import datetime
import socket
import time
import pytest

from PGL.PGLJourney import PGLJourney

from PGL.PGLZoneController import PGLZoneController
from PGL.PGLModel import PGLModel, PGLZigbeeDevice

from PGL.PGLZigbee2mqttClient import PGLZigbee2mqttClient
from PGL.PGLZigbee2mqttClient import PGLZigbee2mqttMessage, PGLZigbee2mqttMessageType
from PGL.PGLZoneController import PGLZoneController
from PGL.PGLController import PGLController

def test_led_map():
    # Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR4_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR5_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led"),
                       PGLZigbeeDevice("LED4_Pigeon", "led"),
                       PGLZigbeeDevice("LED5_Pigeon", "led"),])
    
    zone_controller = PGLZoneController(devices_model)

    # Case 1
    zone_controller.set_device_led_states((1, 4))
    led_states = zone_controller.led_states
    led_states_test = {'LED1_Pigeon': 'ON', 'LED2_Pigeon': 'OFF', 'LED3_Pigeon': 'OFF', 'LED4_Pigeon': 'ON', 'LED5_Pigeon': 'OFF'}
    assert led_states == led_states_test

    # Case 2
    zone_controller.set_device_led_states((2, 3))
    led_states = zone_controller.led_states
    led_states_test = {'LED1_Pigeon': 'OFF', 'LED2_Pigeon': 'ON', 'LED3_Pigeon': 'ON', 'LED4_Pigeon': 'OFF', 'LED5_Pigeon': 'OFF'}
    assert led_states == led_states_test

def test_all_devices():
    # Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led")])
    
    zone_controller = PGLZoneController(devices_model)
    
    # Test devices map
    zone_devices_map = zone_controller.get_zones_devices_map()
    test_map = {1: {"pir": "PIR1_Pigeon", "led": "LED1_Pigeon"},
                2: {"pir": "PIR2_Pigeon", "led": "LED2_Pigeon"},
                3: {"pir": "PIR3_Pigeon", "led": "LED3_Pigeon"}}
    assert zone_devices_map == test_map

    # Test get_zone_from_device_id
    assert zone_controller.get_zone_from_device_id("PIR1_Pigeon") == 1
    assert zone_controller.get_zone_from_device_id("PIR2_Pigeon") == 2
    assert zone_controller.get_zone_from_device_id("PIR3_Pigeon") == 3
    assert zone_controller.get_zone_from_device_id("LED1_Pigeon") == 1
    assert zone_controller.get_zone_from_device_id("LED2_Pigeon") == 2
    assert zone_controller.get_zone_from_device_id("LED3_Pigeon") == 3

def test_light_functions():
    # Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led")])

    zone_controller = PGLZoneController(devices_model)

    # get_device_id_from_zone_id
    print("get_device_id_from_zone_id ok?")
    d1 = zone_controller.get_device_id_from_zone_id(1, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(1, "led")
    assert d1 == "PIR1_Pigeon", "get_device_id_from_zone_id failed"
    assert d2 == "LED1_Pigeon", "get_device_id_from_zone_id failed"
    d1 = zone_controller.get_device_id_from_zone_id(2, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(2, "led")
    assert d1 == "PIR2_Pigeon", "get_device_id_from_zone_id failed"
    assert d2 == "LED2_Pigeon", "get_device_id_from_zone_id failed"
    d1 = zone_controller.get_device_id_from_zone_id(3, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(3, "led")
    assert d1 == "PIR3_Pigeon", "get_device_id_from_zone_id failed"
    assert d2 == "LED3_Pigeon", "get_device_id_from_zone_id failed"

    # get_device_ids_from_zone_ids
    print("get_device_ids_from_zone_ids ok?")
    device_ids = zone_controller.get_device_ids_from_zone_ids([1, 2, 3], ["pir", "pir", "pir"])
    assert device_ids == ['PIR1_Pigeon', 'PIR2_Pigeon', 'PIR3_Pigeon'], "get_device_ids_from_zone_ids failed"
    device_ids = zone_controller.get_device_ids_from_zone_ids([1, 2, 3], ["led", "pir", "pir"])
    assert device_ids == ['LED1_Pigeon', 'PIR2_Pigeon', 'PIR3_Pigeon'], "get_device_ids_from_zone_ids failed"
    device_ids = zone_controller.get_device_ids_from_zone_ids([1, 2, 3], ["pir", "led", "led"])
    assert device_ids == ['PIR1_Pigeon', 'LED2_Pigeon', 'LED3_Pigeon'], "get_device_ids_from_zone_ids failed"


# ------------------------------------------------------------------------------------------------------------------------------



def test_enter_zone():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    journey.enter_zone(1)
    assert journey._PGLJourney__current_zone == 1
    assert journey._PGLJourney__zone_times == {1: [journey._PGLJourney__zone_times[1][0]]}
    assert journey._PGLJourney__milestones == {'complete': False, 'bathroom': False}

    time.sleep(1)  # Wait for 1 second

    journey.enter_zone(2)
    assert journey._PGLJourney__current_zone == 2
    assert journey._PGLJourney__zone_times == {1: [journey._PGLJourney__zone_times[1][0]], 2: [journey._PGLJourney__zone_times[2][0]]}
    assert journey._PGLJourney__milestones == {'complete': False, 'bathroom': False}

    time.sleep(1)  # Wait for 1 second

    journey.enter_zone(1)
    assert journey._PGLJourney__current_zone == 1
    assert journey._PGLJourney__zone_times == {1: [journey._PGLJourney__zone_times[1][0], journey._PGLJourney__zone_times[1][1]], 2: [journey._PGLJourney__zone_times[2][0]]}
    assert journey._PGLJourney__milestones == {'complete': True, 'bathroom': False}

def test_get_journey_to_string():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    journey.enter_zone(1)
    journey.enter_zone(2)
    journey.enter_zone(1)
    journey.enter_zone(3)
    journey.enter_zone(4)
    journey.enter_zone(5)
    journey.enter_zone(4)
    journey.enter_zone(3)
    journey.enter_zone(2)
    journey.enter_zone(1)

    start_time = journey._PGLJourney__zone_times[1][0]
    journey_time = journey._PGLJourney__zone_times[1][-1] - start_time
    bathroom_time = journey._PGLJourney__get_bathroom_time()
    expected_string = f"{start_time}; {journey_time}; {bathroom_time};{socket.gethostname()};"

    obtained_string = journey.get_journey_to_string()
    obtained_parts = obtained_string.split(";")

    assert obtained_parts[0].strip() == start_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    assert obtained_parts[1].strip() == str(journey_time)
    assert obtained_parts[2].strip() == str(bathroom_time)
    assert obtained_parts[3].strip() == socket.gethostname()

    assert journey.is_journey_complete()  # Check if the journey is complete

    journey = PGLJourney(5, lambda x, y: None)  # Reset the journey to start a new one

    journey.enter_zone(5)
    obtained_string = journey.get_journey_to_string()

    assert obtained_string.strip() == "No journey"  # Check if obtained_string is exactly equal to "No journey"
    assert not journey.is_journey_complete()  # Check if the journey is no longer complete


# ------------------------------------------------------------------------------
def test_get_bathroom_time_with_bathroom():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    # Simulate entering and exiting zones
    journey.enter_zone(1)
    journey.enter_zone(2)
    journey.enter_zone(3)
    journey.enter_zone(4)
    journey.enter_zone(5)

    # Set the bathroom milestone using setattr()
    setattr(journey, '_PGLJourney__milestones', {'bathroom': True})

    bathroom_time = journey._PGLJourney__get_bathroom_time()

    if isinstance(bathroom_time, datetime.timedelta):
        assert bathroom_time.total_seconds() >= 0
    else:
        assert bathroom_time == 'N/A'

def test_get_bathroom_time_without_bathroom():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    # Simulate entering and exiting zones
    journey.enter_zone(1)
    journey.enter_zone(2)
    journey.enter_zone(3)
    journey.enter_zone(4)
    journey.enter_zone(5)

    # Simulate no bathroom break
    bathroom_time = journey._PGLJourney__get_bathroom_time()

    assert bathroom_time == 'N/A'

def test_get_bathroom_time_with_multiple_entries():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    # Simulate entering and exiting zones
    journey.enter_zone(1)
    journey.enter_zone(2)
    journey.enter_zone(3)
    journey.enter_zone(4)
    journey.enter_zone(5)

    # Set the bathroom milestone using setattr()
    setattr(journey, '_PGLJourney__milestones', {'bathroom': True})

    bathroom_time = journey._PGLJourney__get_bathroom_time()

    if isinstance(bathroom_time, datetime.timedelta):
        assert bathroom_time.total_seconds() >= 0
    else:
        assert bathroom_time == 'N/A'

def test_get_bathroom_time_with_no_entries():
    journey = PGLJourney(5, lambda x, y: None)  # Replace lambda function with your server API callback

    # Simulate no entries into the previous zone
    bathroom_time = journey._PGLJourney__get_bathroom_time()

    assert bathroom_time == 'N/A'


# -------------------------------------------------------------------------
# Test cases for PGLZoneController:

@pytest.fixture
def zone_controller():
    # Create a PGLModel with sample devices for testing
    devices_model = PGLModel()
    devices_model.sensors_list.append(PGLZigbeeDevice(id_='pir1', type_='pir'))
    devices_model.actuators_list.append(PGLZigbeeDevice(id_='led1', type_='led'))

    # Create a PGLZoneController instance
    return PGLZoneController(devices_model=devices_model)

def test_bind_device_to_zone(zone_controller):
    zone_controller.bind_device_to_zone(zone_id=1, device=PGLZigbeeDevice(id_='pir1', type_='pir'))
    zone_controller.bind_device_to_zone(zone_id=2, device=PGLZigbeeDevice(id_='led1', type_='led'))

    # Check if devices are correctly bound to zones
    assert zone_controller.zones_devices_map[1] == {'pir': 'pir1'}
    assert zone_controller.zones_devices_map[2] == {'led': 'led1'}

def test_get_zone_from_device_id_with_invalid_key():
    controller = PGLZoneController()
    zone = controller.get_zone_from_device_id("invalid_device_id")
    expected_zone = -1  # Default value when key is not found
    assert zone == expected_zone

def test_get_device_id_from_zone_id_with_valid_key():
    controller = PGLZoneController()
    controller.bind_device_to_zone(zone_id=1, device=PGLZigbeeDevice(id_='device1', type_='pir'))
    controller.bind_device_to_zone(zone_id=2, device=PGLZigbeeDevice(id_='device2', type_='led'))
    device_id = controller.get_device_id_from_zone_id(zone_id=1, device_type='pir')
    expected_device_id = 'device1'
    assert device_id == expected_device_id

def test_get_device_ids_from_zone_ids_with_valid_keys():
    controller = PGLZoneController()
    controller.bind_device_to_zone(zone_id=1, device=PGLZigbeeDevice(id_='device1', type_='pir'))
    controller.bind_device_to_zone(zone_id=2, device=PGLZigbeeDevice(id_='device2', type_='led'))
    device_ids = controller.get_device_ids_from_zone_ids(zone_ids=[1, 2], types=['pir', 'led'])
    expected_device_ids = ['device1', 'device2']
    assert device_ids == expected_device_ids


def test_get_zones_devices_map(zone_controller):
    zone_devices_map = zone_controller.get_zones_devices_map()

    # Check if the returned zone_devices_map matches the internal zones_devices_map
    assert zone_devices_map == zone_controller.zones_devices_map

