from .base import Base
from sqlalchemy import Integer, String, DateTime, Column


class SerialStory(Base):
    __tablename__ = 'serial_stories'
    id = Column(Integer(), primary_key=True)
    label = Column(String(), nullable=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
