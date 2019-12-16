from .mysql import MySQL

class DataStoreFactory(object):
    _dao = None

    @classmethod
    def get_instance(cls):
        if not cls._dao:
            cls._dao = MySQL()

        return cls._dao
