from .base import Base
from sqlalchemy import Integer, DateTime, Column


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
