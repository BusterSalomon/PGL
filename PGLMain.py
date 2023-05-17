from time import sleep
from datetime import datetime
from PGLController import PGLController
from PGLModel import PGLModel, PGLZigbeeDevice

START_TIME = 10
END_TIME = 22

if __name__ == "__main__":

    # Create a data model and add a list of known Zigbee devices.
    devices_model = PGLModel()
    devices_model.add([PGLZigbeeDevice("PIR1_PIGEON", "pir"),
                       PGLZigbeeDevice("LED1_PIGEON", "led"),
                       PGLZigbeeDevice("PIR2_PIGEON", "pir"),
                       PGLZigbeeDevice("LED2_PIGEON", "led"),
                       PGLZigbeeDevice("PIR3_PIGEON", "pir"),
                       PGLZigbeeDevice("LED3_PIGEON", "led"),
                       PGLZigbeeDevice("PIR4_PIGEON", "pir"),
                       PGLZigbeeDevice("LED4_PIGEON", "led")])

    while True:
        # if time is between start_time and end_time, start the controller
        if datetime.now().hour >= START_TIME or datetime.now().hour < END_TIME:
            # Create a controller and give it the data model that was instantiated.
            controller = PGLController(devices_model)
            controller.start()

            print("Waiting for events...")
            while True:
                sleep(5)
                # if time is between END_TIME and START_TIME, stop the controller
                if datetime.now().hour >= END_TIME and datetime.now().hour < START_TIME:
                    controller.stop()
                    break
        print(f"Not between {START_TIME} and {END_TIME}, stopping controller...")
        # wait 30 seconds before trying checking the time again
        print("Waiting for 30 seconds...")
        sleep (30)