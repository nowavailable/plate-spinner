class DaoBase(object):
    def session(self):
        pass


    def store_runnning(self):
        pass


    def remove_runnning(self):
        pass


    def build_dequeue_query(self, specified_jobnames=[], sharding_keys=[]):
        pass


    def store_taken_at(self):
        pass


    def store_finished_at(self):
        pass


    def check_killswitch(self):
        pass
