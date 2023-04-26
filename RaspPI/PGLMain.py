from time import sleep
from PGLController import PGLController
from PGLModel import PGLModel, PGLZigbeeDevice


if __name__ == "__main__":
    # Create a data model and add a list of known Zigbee devices.
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_PIGEON", "pir"),
                       PGLZigbeeDevice("LED1_PIGEON", "led")])

    # Create a controller and give it the data model that was instantiated.
    controller = PGLController(devices_model)
    controller.start()

    print("Waiting for events...")

    while True:
        sleep(1)

    controller.stop()
