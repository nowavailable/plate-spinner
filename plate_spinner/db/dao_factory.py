from .dao_mysql import DaoMySQL

class DaoFactory(object):
    _dao = None

    @classmethod
    def get_instance(cls, config):
        if not cls._dao:
            cls._dao = DaoMySQL(config)

        return cls._dao
