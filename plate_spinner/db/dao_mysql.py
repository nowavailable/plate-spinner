from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .dao_base import DaoBase

engine = create_engine('mysql+pymysql://root:@localhost/plate_spinner?charset=utf8mb4', echo=True)

class DaoMySQL(DaoBase):
    def __init__(self, config):
        # TODO: engineをインスタンス変数にして
        # 渡されたconfigを利用するようにする。
        self.session = sessionmaker(bind=engine, expire_on_commit=False)


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
