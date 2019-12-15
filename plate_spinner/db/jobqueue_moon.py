from sqlalchemy import Integer, String, DateTime, JSON, Column
from sqlalchemy.orm import relationship, backref
from .base import Base


class JobQueueMoon(Base):
    __tablename__ = "ps_jobqueue_moons"
    id = Column(Integer(), primary_key=True)
    job_takens = relationship("JobTakenMoon")

    job_name = Column(String(), nullable=False)
    parameters = Column(JSON())
    sharding_keystr = Column(String())
    ready_at = Column(DateTime(), nullable=False)
    finished_at = Column(DateTime())
    created_at = Column(DateTime(), nullable=False)
