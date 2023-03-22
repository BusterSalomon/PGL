from time import sleep
from PGLController import PGLController
from PGLModel import PGLModel, PGLZigbeeDevice


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR2_Pigeon", "pir"),
                       PGLZigbeeDevice("PIR3_Pigeon", "pir"),
                       PGLZigbeeDevice("LED1_Pigeon", "led"),
                       PGLZigbeeDevice("LED2_Pigeon", "led"),
                       PGLZigbeeDevice("LED3_Pigeon", "led"),
                       PGLZigbeeDevice("VR1_Pigeon", "vr")])

    # Create a controller and give it the data model that was instantiated.
    controller = PGLController(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
