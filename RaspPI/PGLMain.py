from time import sleep
from datetime import datetime
from PGLController import PGLController
from PGLModel import PGLModel, PGLZigbeeDevice


if __name__ == "__main__":
    start_time = 9
    end_time = 22

    # Create a data model and add a list of known Zigbee devices.
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_PIGEON", "pir"),
                       PGLZigbeeDevice("LED1_PIGEON", "led"),
                       PGLZigbeeDevice("PIR2_PIGEON", "pir"),
                       PGLZigbeeDevice("LED2_PIGEON", "led"),
                       PGLZigbeeDevice("PIR3_PIGEON", "pir"),
                       PGLZigbeeDevice("LED3_PIGEON", "led")])

    while True:
        # if time is between 22:00 and 09:00, start the controller
        if datetime.now().hour >= end_time or datetime.now().hour < start_time:
            # Create a controller and give it the data model that was instantiated.
            controller = PGLController(devices_model)
            controller.start()

            print("Waiting for events...")
            while True:
                sleep(1)
                # if time is between 09:00 and 22:00, stop the controller
                if datetime.now().hour >= start_time and datetime.now().hour < end_time:
                    controller.stop()
                    break
        print("Not between 22:00 and 09:00, stopping controller...")
        # wait 30 seconds before trying checking the time again
        print("Waiting for 30 seconds...")
        sleep (30)
