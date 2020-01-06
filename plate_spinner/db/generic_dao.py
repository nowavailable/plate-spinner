from datetime import datetime

class GenericDao(object):
    def session(self):
        pass

    def get_entities_by_mode(self):
        return [None, None, None, None]

    def check_mode(self):
        pass

    def check_mode_in_running(self, running):
        return None

    def store_running(self, config):
        return None

    def remove_running(self):
        pass

    def dequeue(self, specified_jobnames=[], sharding_keys=[], limit=5):
        return []

    def store_taken_at(self, dequeued_list):
        pass

    def store_finished_at(self):
        pass

    def check_killswitch(self):
        return None
