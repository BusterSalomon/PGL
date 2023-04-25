# Change path to root of project
import sys
sys.path.append('RaspPI')

# Imports
from PGLZoneController import PGLZoneController
from PGLModel import PGLModel, PGLZigbeeDevice

def main ():
    # test_all_devices()
    # test_some_devices()
    test_light_functions()
    
def test_all_devices ():
    #Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led")])
    
    zone_controller = PGLZoneController(3, devices_model)
    
    # Test devices map
    zone_devices_map = zone_controller.get_zones_devices_map()
    test_map = {0: {"pir": "PIR1_Pigeon",
                    "led": "LED1_Pigeon"},
                1: {"pir": "PIR2_Pigeon",
                    "led": "LED2_Pigeon"},
                2: {"pir": "PIR3_Pigeon",
                    "led": "LED3_Pigeon"},
                }
    print("zone_devices_map ok?")
    print(zone_devices_map == test_map)

    # Test get_zone_from_device_id
    print("get_zone_from_device_id ok?")
    print(zone_controller.get_zone_from_device_id("PIR1_Pigeon") == 0)
    print(zone_controller.get_zone_from_device_id("PIR2_Pigeon") == 1)
    print(zone_controller.get_zone_from_device_id("PIR3_Pigeon") == 2)
    print(zone_controller.get_zone_from_device_id("LED1_Pigeon") == 0)
    print(zone_controller.get_zone_from_device_id("LED2_Pigeon") == 1)
    print(zone_controller.get_zone_from_device_id("LED3_Pigeon") == 2)

def test_some_devices ():
    #Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),])
    
    zone_controller = PGLZoneController(3)
    
    # Manual binding
    zone_controller.bind_device_to_zone(0, devices_model.find("PIR1_Pigeon"))
    zone_controller.bind_device_to_zone(2, devices_model.find("PIR3_Pigeon"))
    zone_controller.bind_device_to_zone(0, devices_model.find("LED1_Pigeon"))
    zone_controller.bind_device_to_zone(1, devices_model.find("LED2_Pigeon"))

    # Test devices map
    zone_devices_map = zone_controller.get_zones_devices_map()
    test_map = {0: {"pir": "PIR1_Pigeon",
                    "led": "LED1_Pigeon"},
                1: {"led": "LED2_Pigeon"},
                2: {"pir": "PIR3_Pigeon"}}
    print("zone_devices_map ok?")
    print(zone_devices_map == test_map)

    # Test get_zone_from_device_id
    print("get_zone_from_device_id ok?")
    print(zone_controller.get_zone_from_device_id("PIR1_Pigeon") == 0)
    print(zone_controller.get_zone_from_device_id("PIR2_Pigeon") == -1)
    print(zone_controller.get_zone_from_device_id("PIR3_Pigeon") == 2)
    print(zone_controller.get_zone_from_device_id("LED1_Pigeon") == 0)
    print(zone_controller.get_zone_from_device_id("LED2_Pigeon") == 1)
    print(zone_controller.get_zone_from_device_id("LED3_Pigeon") == -1)


def test_light_functions ():
    #Instantiate model
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led")])
    
    zone_controller = PGLZoneController(3, devices_model)

    # get_device_id_from_zone_id
    print("get_device_id_from_zone_id ok?")
    d1 = zone_controller.get_device_id_from_zone_id(0, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(0, "led")
    print(d1 == "PIR1_Pigeon")
    print(d2 == "LED1_Pigeon")
    d1 = zone_controller.get_device_id_from_zone_id(1, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(1, "led")
    print(d1 == "PIR2_Pigeon")
    print(d2 == "LED2_Pigeon")
    d1 = zone_controller.get_device_id_from_zone_id(2, "pir")
    d2 = zone_controller.get_device_id_from_zone_id(2, "led")
    print(d1 == "PIR3_Pigeon")
    print(d2 == "LED3_Pigeon")

    # get_device_ids_from_zone_ids
    print("get_device_ids_from_zone_ids ok?")
    device_ids = zone_controller.get_device_ids_from_zone_ids([0, 1, 2], ["pir", "pir", "pir"])
    print(device_ids == ['PIR1_Pigeon', 'PIR2_Pigeon', 'PIR3_Pigeon'])
    device_ids = zone_controller.get_device_ids_from_zone_ids([0, 1, 2], ["led", "pir", "pir"])
    print(device_ids == ['LED1_Pigeon', 'PIR2_Pigeon', 'PIR3_Pigeon'])
    device_ids = zone_controller.get_device_ids_from_zone_ids([0, 1, 2], ["pir", "led", "led"])
    print(device_ids == ['PIR1_Pigeon', 'LED2_Pigeon', 'LED3_Pigeon'])


if __name__ == "__main__":
    main()

