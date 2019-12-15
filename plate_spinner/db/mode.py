from sqlalchemy import Integer, String, DateTime, Boolean, Column
from .base import Base


class Mode(Base):
    __tablename__ = 'ps_models'
    id = Column(Integer(), primary_key=True)
    mode = Column(String(), nullable=False)
