from .base import Base
from sqlalchemy import Integer, String, DateTime, JSON, Column, ForeignKey
from sqlalchemy.orm import relationship


class Pivot(Base):
    __tablename__ = 'pivots'
    id = Column(Integer(), primary_key=True)
    serial_story_id = Column(Integer(), ForeignKey("serial_stories.id"))
    serial_story = relationship("SerialStory")

    uri = Column(String(), nullable=False)
    analyzed = Column(JSON())
    transaction_key = Column(String())
    taker_key = Column(String())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)

