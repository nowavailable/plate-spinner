from .base import Base
from sqlalchemy import Integer, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship, backref


class JobTakenMoon(Base):
    __tablename__ = "ps_job_taken_moons"
    id = Column(Integer(), primary_key=True)
    jobqueue_id = Column(Integer(), ForeignKey("ps_jobqueue_moons.id"), name="ps_jobqueue_moon_id")
    jobqueue = relationship("JobQueueMoon")

    created_at = Column(DateTime(), nullable=False)

