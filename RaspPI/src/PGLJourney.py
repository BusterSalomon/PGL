# Import time modules
import datetime
from threading import Event, Thread
import socket
from time import sleep


class PGLJourney:
    """ Class for handling the timing and milestones of a journey.

    A Journey is a defined as a roundtrip from zone 1 to the last zone and back to zone 1.
    The journey is timed and the time spent in the bathroom is also timed.
    A thread is started when journey is created, to check if time limit has been 
    exceeded in bathroom, thus potentially a fall has occurred.
    """

    def __init__(self, last_zone: int, server_api_callback):
        self.__zone_times = {}  # {zone: [times]}
        self.__milestones = {'complete': False, 'bathroom': False}
        self.__current_zone = None
        self.__last_zone = last_zone
        self.server_api_callback = server_api_callback
        self.__timeout = datetime.timedelta(seconds=60)

        # Threading
        self.stop_worker = Event()
        self.__time_limit: datetime.timedelta = datetime.timedelta(seconds=600)
        self.__timer_thread = Thread(target=self.timing_worker, daemon=True)
        self.__timer_thread.start()

    def enter_zone(self, zone: int) -> None:
        """ Enters the given zone and updates the journey object"""

        # if time since last zone is less than timeout, reset journey.
        if self.__current_zone is not None:
            time_delta = datetime.datetime.now(
            ) - self.__zone_times[self.__current_zone][-1]
            if time_delta > self.__timeout:
                self.__zone_times = {}  # {zone: [times]}
                self.__milestones = {'complete': False, 'bathroom': False}
                self.__current_zone = None

        self.__current_zone = zone  # mutex maybe?

        latest_timestamp = datetime.datetime.now()
        if zone in self.__zone_times:
            self.__zone_times[zone].append(latest_timestamp)
        else:
            self.__zone_times[zone] = [latest_timestamp]

        # Validate roundtrip
        # If not the first entrance (start) and the zone added is zero
        self.__set_milestones_if_complete(zone)

    def get_journey_to_string(self) -> str:
        """ Returns the journey as a string. 

        Formatted as:
        <start_time>; <journey_time>; <bathroom_time>; <raspberry_pi_id>
        Returns "No journey" if the journey is not complete.
        """
        if not self.__zone_times:  # If the journey is empty
            return "No journey"
        journey_time = self.__zone_times[1][-1] - self.__zone_times[1][0]
        bathroom_time = self.__get_bathroom_time()
        #READ: Should we use hostname or serial number of pi? https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
        journey_string = f"{self.__zone_times[1][0]}; {journey_time}; {bathroom_time};{socket.gethostname()}; "
        return journey_string

    def __get_bathroom_time(self) -> datetime.timedelta:
        """ Returns the time spent in the bathroom."""
        bathroom_time = None
        if self.__milestones['bathroom']:
            bathroom_start = self.__zone_times[self.__last_zone][0]
            bathroom_end = None
            for time in self.__zone_times[self.__last_zone - 1]:
                if time >= bathroom_start:
                    bathroom_end = time
                    break
            bathroom_time = bathroom_end - bathroom_start
        else:
            bathroom_time = 'N/A'
        return bathroom_time

    def __set_milestones_if_complete(self, zone) -> None:
        # If the journey is not empty and the current zone is 1 then the journey is complete
        if (len(self.__zone_times) != 1 and zone == 1):
            self.__milestones['complete'] = True
            if self.__last_zone in self.__zone_times:  # If the last zone is in the zone_times
                self.__milestones['bathroom'] = True

    def is_journey_complete(self) -> bool:
        """ Returns true if the journey is complete, and bathroom has been visited. """
        return self.__milestones['complete'] and self.__milestones['bathroom']

    def timing_worker(self) -> None:
        """ Worker that checks if the time limit has been exceeded. 

        Runs in a separate thread. 
        Checks if the time limit has been exceeded, every 10 seconds.
        """
        while not self.stop_worker.is_set():
            time_passed = self.__get_time_passed_in_bathroom()

            # If time limit have exceeded, call callback
            if time_passed > self.__time_limit:
                tmp_string = str(datetime.datetime.now()) + ";" + str(time_passed)+ ";" + socket.gethostname() + ";"
                print(tmp_string)
                self.server_api_callback(tmp_string, "emergency")
            sleep(10)

    def __set_milestones_if_complete(self, zone) -> None:
        """ Sets the milestones if the journey, depending on what is done. """
        # If the journey is not empty and the current zone is 0 then the journey is complete
        if (len(self.__zone_times) != 1 and zone == 1):
            self.__milestones['complete'] = True
            if self.__last_zone in self.__zone_times:  # If the last zone is in the zone_times
                self.__milestones['bathroom'] = True

    def __get_time_passed_in_bathroom(self) -> datetime.timedelta:
        """ Returns the time passed in the bathroom."""
        time_passed: datetime.timedelta = datetime.timedelta(0)
        if self.__last_zone == self.__current_zone:
            time_passed = datetime.datetime.now(
            ) - self.__zone_times[self.__last_zone][0]
        return time_passed
