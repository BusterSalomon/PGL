from paho.mqtt.client import Client as MqttClient, MQTTMessage
from threading import Event, Thread
from queue import Empty, Queue
from dataclasses import dataclass
from time import sleep

@dataclass
class Event_:
    """ Dataclass for events to be sent to the server."""
    type : str
    payload : str

class PGLServerAPI:
    """ Class for the server api. 
    
    Handles the communication with the server.
    Using MQTT protocol.
    """

    __EMERGENCY_TYPE = "emergency"
    __JOURNEY_TYPE = "journey"
    __REQUEST_STORE_EVENT_IN_DB_TOPIC = 'PGL/request/store_event'
    __REQUEST_EMERGENCY_TOPIC = 'PGL/request/emergency'

    def __init__(self, mqtt_host : str, mqtt_port : int = 1883) -> None:
        self.__mqtt_host = mqtt_host
        self.__mqtt_port = mqtt_port
        self.__mqtt_client = MqttClient()

        # initialize callback methods
        self.__mqtt_client.on_connect = self.__on_connect
        self.__mqtt_client.connect(host=self.__mqtt_host,  # connect to mqtt
                                   port=self.__mqtt_port)
        self.__mqtt_client.loop_start()                     # start loop
        self.__events_queue = Queue()
        self.__stop_worker = Event()
        self.__worker_thread = Thread(target=self.__worker,
                                      daemon=True)



    def __on_connect(self, client, userdata, flags, rc) -> None:
        """ Callback method for when the client connects to the broker."""
        print("ServerAPI client connected \n")
        self.__worker_thread.start()


    def add_event_to_queue(self, payload : str, event_type : str) -> None:
        """ Adds an event to the queue."""
        new_event = Event_(event_type, payload)
        self.__events_queue.put(new_event)

    def stop_server_api(self):
        """ Stops the server api."""
        self.__stop_worker.set()
        self.__mqtt_client.loop_stop()
        self.__mqtt_client.disconnect()

    def __worker(self) -> None:
        """ Worker method for the server api.
        
        Checks for events in the queue and publishes them to the server to.
        """
        print("ServerAPI worker started \n")
        while not self.__stop_worker.is_set():
            incoming_event : Event_ = None
            try:
                if self.__mqtt_client.is_connected():
                    incoming_event = self.__events_queue.get(timeout=1)
                else:
                    sleep(0.02)

            except Empty:
                pass

            else:
                try:
                    if incoming_event.type == self.__EMERGENCY_TYPE:
                        self.__mqtt_client.publish(self.__REQUEST_EMERGENCY_TOPIC,
                                                   incoming_event.payload)
                        print("ServerAPI: Published emergency")
                    elif incoming_event.type == self.__JOURNEY_TYPE:
                        self.__mqtt_client.publish(self.__REQUEST_STORE_EVENT_IN_DB_TOPIC,
                                                   incoming_event.payload)
                        print("ServerAPI: Published journey")

                except KeyError:
                    print(f'Error occurred in API_worker: {KeyError}')
