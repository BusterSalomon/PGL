from paho.mqtt.client import Client as MqttClient, MQTTMessage
from threading import Event, Thread
from queue import Empty, Queue
from dataclasses import dataclass
from time import sleep

@dataclass
class Event_:
        type : str
        payload : str

class PGLServerAPI:

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
        
        self.__worker_thread.start()

    def __on_connect(self, client, userdata, flags, rc) -> None:
        print("ServerAPI client connected \n")
        

    def add_event_to_queue(self, payload : str, type : str) -> None:
        new_event = Event_(type, payload)
        self.__events_queue.put(new_event)

    def stop_server_api(self):
        self.__stop_worker.set()
        self.__mqtt_client.loop_stop()
        self.__mqtt_client.disconnect()

    def __worker(self) -> None:
        print("ServerAPI worker started \n")
        while not self.__stop_worker.is_set():
            try:
                if self.__mqtt_client.is_connected():
                    incoming_event : Event_ = self.__events_queue.get(timeout=1)
                else:
                    sleep(0.02)

            except Empty:
                print('ServerAPI worker: queue is empty')
                pass

            else:
                try:
                    if incoming_event.type == self.__EMERGENCY_TYPE:
                        self.__mqtt_client.publish(self.__REQUEST_EMERGENCY_TOPIC, incoming_event.payload)
                        print("published emergency")
                    elif incoming_event.type == self.__JOURNEY_TYPE:
                        self.__mqtt_client.publish(self.__REQUEST_STORE_EVENT_IN_DB_TOPIC, incoming_event.payload)
                        print("published journey")

                except KeyError:
                    print(f'Error occured in API_worker: {KeyError}')

        