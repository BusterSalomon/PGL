# Import time modules
import calendar
import time
from threading import Event, Thread



class PGLJourney:

    def __init__(self, last_zone):
        self.zone_times = {} # {zone: [times]}
        self.milestones = {'complete': False, 'bathroom': False}
        self.last_zone = last_zone


        # Threading
        # self.__timer_thread = Thread(target=self.timing_worker, daemon=True)
        # self.__timer_thread.start()


    def enter_zone (self, zone):
        self.latest_timestamp = self.get_timestamp()
        if self.zone_times[zone] is None:
            self.zone_times[zone] = [self.latest_timestamp]
        else:
            self.zone_times[zone].append(self.latest_timestamp)

        # Validate roundtrip
        # If not the first entrance (start) and the zone added is zero
        if (len(self.zone_times) != 1 and zone == 0): # to do: logic for if bathroom has been visited
            self.milestones['complete'] = True 
            if self.last_zone in self.zone_times:
                self.milestones['bathroom'] = True
    
    def get_journey_to_string (self):
        journey_time = self.zone_times[0][-1] - self.zone_times[0][0]
        bathroom_time = self.zone_times[self.last_zone][0]
        for time in 
        journey_string += f"date: {self.zone_times[0][0]};"
        
             

    def get_milestones (self) -> bool:
        return self.milestones
    
    def timing_worker (self):
        # Get timelimit for zone
        _, current_zone = self.zone_times[-1]
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
    

















