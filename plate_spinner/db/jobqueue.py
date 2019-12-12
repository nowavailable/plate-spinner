from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class JobQueue(Base):
    __tablename__ = 'pr_jobqueues'
