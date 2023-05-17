from PGL.PGLModel import PGLModel
# from PGLWebClient import PGLWebClient, PGLWebDeviceEvent
from PGL.PGLZigbee2mqttClient import (PGLZigbee2mqttClient,
                                  PGLZigbee2mqttMessage, PGLZigbee2mqttMessageType)

# import zone controller
from PGL.PGLZoneController import PGLZoneController
a = PGLModel


class PGLController:
    """ The controller is responsible for managing events received from zigbee2mqtt and handle them.
    By handle them it can be process, store and communicate with other parts of the system. In this
    case, the class listens for zigbee2mqtt events, processes them (turn on another Zigbee device)
    and send an event to a remote HTTP server.
    """

    MQTT_BROKER_HOST = "localhost"
    MQTT_BROKER_PORT = 1883

    def __init__(self, devices_model: PGLModel) -> None:
        """ Class initializer. The actuator and monitor devices are loaded (filtered) only when the
        class is instantiated. If the database changes, this is not reflected.

        Args:
            devices_model (PGLModel): the model that represents the data of this application
        """
        self.__devices_model = devices_model
        self.__z2m_client = PGLZigbee2mqttClient(host=self.MQTT_BROKER_HOST,
                                                 port=self.MQTT_BROKER_PORT,
                                                 on_message_clbk=self.__zigbee2mqtt_event_received)

        # initialize zone controller object and tim
        self.__zone_controller = PGLZoneController(self.__devices_model)

    def start(self) -> None:
        """ Start listening for zigbee2mqtt events.
        """
        self.__z2m_client.connect()

        print(f"Zigbee2Mqtt is {self.__z2m_client.check_health()}")

    def stop(self) -> None:
        """ Stop listening for zigbee2mqtt events.
        """
        self.__z2m_client.disconnect()


    def __zigbee2mqtt_event_received(self, message: PGLZigbee2mqttMessage) -> None:
        """ Process an event received from zigbee2mqtt. This function given as callback to
        PGLZigbee2mqttClient, which is then called when a message from zigbee2mqtt is received.

        Args:
            message (PGLZigbee2mqttMessage): an object with the message received from zigbee2mqtt
        """
        # If message is None (it wasn't parsed), then don't do anything.
        if not message:
            return


        print(
            f"zigbee2mqtt event received on topic {message.topic}: \
                {message.event}, type: {message.type_}")

        # If the message is not a device event, then don't do anything.
        if message.type_ != PGLZigbee2mqttMessageType.DEVICE_EVENT:
            return

        # Parse the topic to retrieve the device ID. If the topic only has one level, don't do
        # anything.

        tokens = message.topic.split("/")
        if len(tokens) <= 1:
            return

        # Retrieve the device ID from the topic.
        device_id = tokens[1]

        # If the device ID is known, then process the device event and send a message to the remote
        # web server.
        device = self.__devices_model.find(device_id)

        # If the type of the event is a motion sensor
        if device.type_ == "pir":
            # reset alarm timer in its own thread, when journey complete stop timer.
            occupancy: bool
            try:
                occupancy = message.event["occupancy"]

            except KeyError:
                pass
            else:
                # Pass data and topic to the zone controller which
                # returns (optional) a journey object and lights to be turned on
                # journey is a dict with the zones and corresponding time interval tuples.
                if occupancy:
                    print(f'{device.id_} says occupancy: {occupancy}')
                    led_state_map = self.__zone_controller.control_zones(device.id_)
                    # Light up zones, and light down old zones
                    self.__z2m_client.change_light_zones_states (led_state_map)
