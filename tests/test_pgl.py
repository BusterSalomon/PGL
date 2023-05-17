# Imports
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

