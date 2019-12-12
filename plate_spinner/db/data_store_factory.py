from .mysql import MySQL

class DataStoreFactory(object):
    _dao = None

    @classmethod
    def get_instance(cls, config):
        if not cls._dao:
            cls._dao = MySQL(config)

        return cls._dao
