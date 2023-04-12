from PGLZoneController import PGLZoneController
from PGLModel import PGLModel, PGLZigbeeDevice
from PGLJourney import Journey

devices_model = PGLModel()
devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                    PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                    PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                    PGLZigbeeDevice("LED1_Pigeon", "led"),
                    PGLZigbeeDevice("LED2_Pigeon", "led"),
                    PGLZigbeeDevice("LED3_Pigeon", "led")])
zone_controller = PGLZoneController(devices_model.devices_list)
journey, lights = zone_controller.control_zones(True, "PIR1_Pigeon")
print(journey)
print(lights)
journey, lights = zone_controller.control_zones(True, "PIR2_Pigeon")
print(journey)
print(lights)
journey, lights = zone_controller.control_zones(True, "PIR3_Pigeon")
print(journey)
print(lights)
journey, lights = zone_controller.control_zones(True, "PIR2_Pigeon")
print(journey)
print(lights)
journey, lights = zone_controller.control_zones(True, "PIR1_Pigeon")
print(journey)
print(lights)

