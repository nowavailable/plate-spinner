from .base import Base
from sqlalchemy import Integer, String, DateTime, Text, JSON, Column, ForeignKey
from sqlalchemy.orm import relationship


class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer(), primary_key=True)
    serial_story_id = Column(Integer(), ForeignKey("serial_stories.id"))
    serial_story = relationship("SerialStory")
    episode_id = Column(Integer(), ForeignKey("episodes.id"))
    parent_episode = relationship("Episode")

    number = Column(Integer(), nullable=False, default=1)
    uri = Column(String(), nullable=False)
    analyzed = Column(JSON())
    content = Column(Text())
    transaction_key = Column(String())
    taker_key = Column(String())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
