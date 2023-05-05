# Change path to root of project
import sys
sys.path.append('RaspPI')

# Imports
from PGLZoneController import PGLZoneController
from PGLModel import PGLModel, PGLZigbeeDevice
from time import sleep

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
# TEST CASE 1: Test journey complete

lights = zone_controller.control_zones("PIR1_Pigeon")
print(lights)
sleep(1)
lights = zone_controller.control_zones("PIR2_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR4_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR5_Pigeon")
print(lights)
sleep(16)
lights = zone_controller.control_zones("PIR4_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR2_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR1_Pigeon")
print(lights)
sleep(1)

sleep(10)
print("\n")

# TEST CASE 2: Emergency when stuck in zone 3
lights = zone_controller.control_zones("PIR1_Pigeon")
print(lights)
sleep(1)
lights = zone_controller.control_zones("PIR2_Pigeon")
print(lights)
sleep(2)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(5)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(8)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(5)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(5)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(5)
lights = zone_controller.control_zones("PIR3_Pigeon")
print(lights)
sleep(5)
