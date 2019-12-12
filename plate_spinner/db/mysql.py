from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base


# TODO: 継承ではなくMix-inで。MySQLはモデルからも使用されるので、DAOであってほしくないから。
class MySQL(Base):

    _engine = None

    def __init__(self, config):
        # TODO: engineをインスタンス変数にして
        # 渡されたconfigを利用するようにする。

        self.session = sessionmaker(bind=MySQL.get_engine(), expire_on_commit=False)


    def session_close(self):
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
        return False

    @classmethod
    def get_engine(cls):
        if not cls._engine:
            cls._engine = create_engine('mysql+pymysql://root:@localhost/plate_spinner?charset=utf8mb4', echo=True)

        return cls._engine