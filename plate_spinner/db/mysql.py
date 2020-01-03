import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, not_
from .generic_dao import GenericDao
from .mode import Mode
from .running import Running
from .jobqueue_sun import JobQueueSun
from .jobqueue_moon import JobQueueMoon
from .job_taken_sun import JobTakenSun
from .job_taken_moon import JobTakenMoon


# TODO: 継承ではなくMix-inで?
class MySQL(GenericDao):

    _engine = None
    _mode = ["Sun", "Moon"]

    def __init__(self):
        self.session = sessionmaker(
            bind=MySQL.get_engine(),
            expire_on_commit=False
        )()
        self.mode = self.__class__._mode[0]

    def get_entities(self):
        if self.mode == self.__class__._mode[0]:
            entity = JobQueueSun
            taken_entity = JobTakenSun
        else:
            entity = JobTakenMoon
            taken_entity = JobTakenMoon

        return [entity, taken_entity]

    """
    制御テーブルである modes テーブルに、一行のレコードが予め登録されていることを期待する。
    そのレコードは、mode カラムに、`Sun` あるいは `Moon`のいずれかの値を保持していること。
    """
    def check_mode(self):
        mode_rows = self.session.query(Mode).all()
        if len(mode_rows) == 0:
            raise RuntimeError("Need to set a record to `modes` table.")
        if mode_rows[0].mode not in __class__._mode:
            raise RuntimeError("Specify mode either `Sun` or `Moon`.")
        self.mode = mode_rows[0].mode

    def store_runnning(self):
        now = datetime.now()
        running = Running(
            hostname=os.uname()[1],
            process_id_str=("%s" % os.getpid()),
            created_at=now,
            updated_at=now
        )
        self.session.add(running)
        # TODO: ログへの書き出し。ひいてはログの設計。

    def remove_runnning(self):
        runnings = self.session.query(Running).filter(
            Running.hostname == os.uname()[1],
            Running.process_id_str == ("%s" % os.getpid()),
            Running.emergency == True
        ).all()
        if len(runnings) > 0:
            self.session.delete(runnings[0])

    def dequeue(self, specified_jobnames=[], sharding_keys=[], limit=5):
        entity, taken_entity = self.get_entities()

        if self.mode == self.__class__._mode[0]:
            entity = JobQueueSun
            taken_entity = JobTakenSun
        else:
            entity = JobTakenMoon
            taken_entity = JobTakenMoon

        now = datetime.now()
        where_list = []
        if len(specified_jobnames) > 0:
            where_list = list(
                map(lambda jobname: (entity.job_name == jobname), specified_jobnames)
            )
        if len(sharding_keys) > 0:
            where_list += list(
                map(lambda sharding_key: (entity.sharding_keystr == sharding_key), sharding_keys)
            )
        if len(where_list) > 0:
            where_list = [entity.job_name != ""]

        return self.session.query(entity). \
            outerjoin(taken_entity). \
            filter(and_(
                entity.ready_at < now,
                entity.finished_at == None,
                taken_entity.id == None
            )). \
            filter(or_(*where_list)). \
            limit(limit).all()

    def store_taken_at(self, dequeued_list):
        entity, taken_entity = self.get_entities()
        now = datetime.now()
        for jobqueue in dequeued_list:
            associated = taken_entity(
                jobqueue = jobqueue,
                created_at = now
            )
            self.session.add(associated)

    def store_finished_at(self):
        pass

    def check_killswitch(self):
        runnings = self.session.query(Running).filter(
            Running.hostname == os.uname()[1],
            Running.process_id_str == ("%s" % os.getpid()),
            Running.emergency == 1
        ).all()
        return len(runnings) > 0

    @classmethod
    def get_engine(cls):
        if not cls._engine:
            # TODO: 環境変数またはそれに代わる方式の利用
            cls._engine = create_engine(
                'mysql+pymysql://root:@localhost/plate_spinner?charset=utf8mb4',
                echo=True,
                isolation_level="READ COMMITTED"
            )

        return cls._engine
