from sqlalchemy import Integer, String, DateTime, Boolean, Column
from .base import Base


class Running(Base):
    __tablename__ = 'ps_runnings'
    id = Column(Integer(), primary_key=True)
    hostname = Column(String(), nullable=False)
    process_id_str = Column(String(), nullable=False)
    emergency = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
