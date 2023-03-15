from time import sleep
from PGLController import PGLController
from PGLModel import PGLModel, PGLZigbeeDevice


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("0x00158d00044c228a", "pir"),
                       PGLZigbeeDevice("0xccccccfffeeaa775", "led"),
                       PGLZigbeeDevice("0xddddddfffeeaa775", "power plug")])

    # Create a controller and give it the data model that was instantiated.
    controller = PGLController(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
