# Import time modules
import calendar
import time
from threading import Event, Thread



class PGLJourney:

    def __init__(self, last_zone : int):
        self.__zone_times = {} # {zone: [times]}
        self.__milestones = {'complete': False, 'bathroom': False}
        self.__last_zone = last_zone


        # Threading
        # self.__timer_thread = Thread(target=self.timing_worker, daemon=True)
        # self.__timer_thread.start()


    def enter_zone (self, zone):
        self.latest_timestamp = self.get_timestamp()
        if self.__zone_times[zone] is None:
            self.__zone_times[zone] = [self.latest_timestamp]
        else:
            self.__zone_times[zone].append(self.latest_timestamp)

        # Validate roundtrip
        # If not the first entrance (start) and the zone added is zero
        if (len(self.__zone_times) != 1 and zone == 0): # to do: logic for if bathroom has been visited
            self.__milestones['complete'] = True 
            if self.__last_zone in self.__zone_times:
                self.__milestones['bathroom'] = True
    
    def get_journey_to_string (self) -> str:
        journey_time = self.__zone_times[0][-1] - self.__zone_times[0][0]
        if self.__milestones['bathroom'] == True:
            bathroom_start = self.__zone_times[self.__last_zone][0]
            for time in self.__zone_times[self.__last_zone - 1]:
                if time > bathroom_start:
                    bathroom_end = time
                    break
            bathroom_time = bathroom_end - bathroom_start
        else:
            bathroom_time = 'N/A'
        journey_string = f"{self.__zone_times[0][0]}; {journey_time}; {bathroom_time};"
        return journey_string 

             

    def get___milestones (self) -> bool:
        return self.__milestones
    
    def timing_worker (self) -> None:
        # Get timelimit for zone
        _, current_zone = self.__zone_times[-1]
        zone_time_limit_s = self.ZONE_TIME_LIMITS[current_zone]
        zone_time_limit_ms = self.seconds_to_milliseconds(zone_time_limit_s)

        # Validate if time limit have exceeded
        current_time: int = self.get_timestamp()
        time_passed: int = current_time - self.latest_timestamp
        time_exceeded : bool = time_passed > zone_time_limit_ms

        # If time limit have exceeded, call callback
        if (time_exceeded):
            self.__exceeded_zone_timelimit_clbk()
    
    # Not tested! https://flexiple.com/python/python-timestamp/
    # calender library might need to be implemented!
    def get_timestamp (self):
        current_GMT = time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        return time_stamp
    
    # NEED IMPLEMENTATION
    def seconds_to_milliseconds(sec: int) -> int:
        return -1
    

















