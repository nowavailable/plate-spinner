from .base import Base
from sqlalchemy import Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class JobTakenSun(Base):
    __tablename__ = "ps_job_taken_suns"
    id = Column(Integer(), primary_key=True)
    jobqueue_id = Column(Integer(), ForeignKey("ps_jobqueue_suns.id"), name="ps_jobqueue_sun_id")
    jobqueue = relationship("JobQueueSun")

    created_at = Column(DateTime(), nullable=False)

