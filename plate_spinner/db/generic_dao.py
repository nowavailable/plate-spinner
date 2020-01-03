from datetime import datetime

class GenericDao(object):
    def session(self):
        pass

    def check_mode(self):
        pass

    def store_runnning(self):
        pass

    def remove_runnning(self):
        pass

    def dequeue(self, specified_jobnames=[], sharding_keys=[], limit=5):
        pass

    def store_taken_at(self, dequeued_list):
        pass

    def store_finished_at(self):
        pass

    def check_killswitch(self):
        pass
