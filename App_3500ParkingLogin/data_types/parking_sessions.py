

class NewParkingSession(dict):
    # class SessionKeys:
    #     REG_DICT = 'reg_dict'
    #     START_TIME = 'start_time'
    #     NEXT_TIME = 'next_time'
    #     COUNT = 'count'
    #     FREQUENCY = 'frequency'
    #
    # keys = SessionKeys()

    def __init__(self, name, reg_dict, start_time, frequency, start_count, one_time=True):
        super().__init__()
        # SESSION DATA
        self.name = name
        self.reg_dict = reg_dict
        self.start_time = start_time
        self.next_time = self.start_time  # START AS START TIME
        self.frequency = frequency
        self.start_count = start_count
        self.count_remaining = self.start_count

        # ONE TIME FLAG - DETERMINES IF THIS WILL CREATE A SESSION OR NOT
        self.one_time = one_time

        # STOP SESSION FLAG
        self.stop_session = False

        # SET INITIAL NEXT TIME IMMEDIATELY
        self.set_next_time()

    def set_next_time(self):
        self.next_time = self.next_time + self.frequency