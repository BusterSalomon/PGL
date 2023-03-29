# Import time modules
import calendar
import time
from threading import Event, Thread


class PGLJourney:
    ZONE_TIME_LIMITS = [10, 10, 10, 10, 10]

    def __init__(self, exceeded_zone_timelimit_clbk):
        # [(timestamp_i, zone_j)]
        self.zone_times = [()]
        self.complete_journey = False
        self.__exceeded_zone_timelimit_clbk = exceeded_zone_timelimit_clbk

        # Threading
        # self.__timer_thread = Thread(target=self.timing_worker, daemon=True)
        # self.__timer_thread.start()


    def enter_zone (self, zone):
        self.latest_timestamp = self.get_timestamp()
        self.zone_times.append((self.latest_timestamp, zone))

        # Validate roundtrip
        # If not the first entrance (start) and the zone added is zero
        if (len(self.zone_times) != 1 and zone == 0):
            self.complete_journey = True

    def get_is_journey_complete (self) -> bool:
        return self.complete_journey
    
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
    
