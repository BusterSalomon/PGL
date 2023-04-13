# Import time modules
import datetime
from threading import Event, Thread



class PGLJourney:

    def __init__(self, last_zone : int):
        self.__zone_times = {} # {zone: [times]}
        self.__milestones = {'complete': False, 'bathroom': False}
        self.__last_zone = last_zone
        self.__current_zone = None


        # Threading
        # self.__timer_thread = Thread(target=self.timing_worker, daemon=True)
        # self.__timer_thread.start()


    def enter_zone (self, zone : int) -> None:
        self.__current_zone = zone # mutex maybe?

        self.latest_timestamp = datetime.datetime.now()
        if self.__zone_times[zone] is None:
            self.__zone_times[zone] = [self.latest_timestamp]
        else:
            self.__zone_times[zone].append(self.latest_timestamp)

        # Validate roundtrip
        # If not the first entrance (start) and the zone added is zero
        if (len(self.__zone_times) != 1 and zone == 0): 
            self.__milestones['complete'] = True 
            if self.__last_zone in self.__zone_times: # If the last zone is in the zone_times
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
        journey_string = f"{self.__zone_times[0][0]}; {journey_time}; {bathroom_time};"    #we should also add the RASPPI id here (last one) perhaps (socket.gethostname())
        return journey_string 

    def is_journey_complete (self) -> bool:
        return self.__milestones['complete'] and self.__milestones['bathroom']
    
    def timing_worker (self, time_limit) -> None:

        # evaluate if time limit have exceeded if user is in the last zone
        if (self.__last_zone == self.__current_zone):
            current_time: int = datetime.datetime.now()
            time_passed: int = current_time - self.__zone_times[self.__last_zone][0]

        # If time limit have exceeded, call callback
        if (time_passed > time_limit):
            pass
    

















