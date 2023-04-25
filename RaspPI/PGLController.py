from PGLModel import PGLModel
# from PGLWebClient import PGLWebClient, PGLWebDeviceEvent
from PGLZigbee2mqttClient import (PGLZigbee2mqttClient,
                                  PGLZigbee2mqttMessage, PGLZigbee2mqttMessageType)

# import zone controller
from PGLZoneController import PGLZoneController


class PGLController:
    HTTP_HOST = "http://localhost:8000"
    MQTT_BROKER_HOST = "localhost"
    MQTT_BROKER_PORT = 1883

    """ The controller is responsible for managing events received from zigbee2mqtt and handle them.
    By handle them it can be process, store and communicate with other parts of the system. In this
    case, the class listens for zigbee2mqtt events, processes them (turn on another Zigbee device)
    and send an event to a remote HTTP server.
    """

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
            f"zigbee2mqtt event received on topic {message.topic}: {message.data}")

        # If the message is not a device event, then don't do anything.
        if message.type_ != PGLZigbee2mqttMessageType.DEVICE_EVENT:
            return

        # Parse the topic to retreive the device ID. If the topic only has one level, don't do
        # anything.

        tokens = message.topic.split("/")
        if len(tokens) <= 1:
            return

        # Retrieve the device ID from the topic.
        device_id = tokens[1]

        # If the device ID is known, then process the device event and send a message to the remote
        # web server.
        device = self.__devices_model.find(device_id)

        if device.type_ == "pir":
            # reset alarm timer in its own thread, when journey complete stop timer.
            try:
                occupancy = message.event["occupancy"]

            except KeyError:
                pass
            else:
                # Pass data and topic to the zone controller which returns (optional) a journey object and lights to be turned on
                # journey is a dict with the zones and corresponding time interval tuples.
                journey, lights = self.__zone_controller.control_zones(
                    message.event["occupancy"], device.id_)

                # Get device id's from zone id's
                device_ids = self.__zone_controller.get_device_ids_from_zone_ids(list(lights), ["led", "led"])

                # Light up zones, and light down old zones
                self.__z2m_client.change_light_zones_states (device_ids, self.__devices_model.actuators_list)

                # Change the state on all actuators, i.e. LEDs and power plugs (NOTE: should be based on 'lights')
                # for i, a in enumerate(self.__devices_model.actuators_list):
                #     self.__z2m_client.change_state(a.id_, lights[i])

                # Register event in the remote web server.
                if journey.complete:  # maybe stop timing thread here
                    pass
                    # PGLWebDeviceEvent()
                    # client = PGLWebClient(self.HTTP_HOST)
                    # try:
                    #     # client.send_event(web_event.to_json())
                    # except ConnectionError as ex:
                    #     print(f"{ex}")

                # Legacy:
                # web_event = PGLWebDeviceEvent(device_id=device.id_,
                #                               device_type=device.type_,
                #                               measurement=occupancy)

                # client = PGLWebClient(self.HTTP_HOST)
                # try:
                #     client.send_event(web_event.to_json())
                # except ConnectionError as ex:
                #     print(f"{ex}")
                #   -----------------------  #

        if device.type_ == "vs":
            pass
            # if we want to detect the door opening as well.
