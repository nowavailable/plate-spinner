from .base import Base
from sqlalchemy import Integer, String, DateTime, Boolean, Column, ForeignKey
from sqlalchemy.orm import relationship

class UriApplied(Base):
    __tablename__ = 'uri_applieds'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey("users.id"))
    user = relationship("User")

    uri = Column(String(), nullable=False)
    proc_fixed = Column(Boolean(), default=False)
    proc_count = Column(Integer(), nullable=False)
    transaction_key = Column(String())
    taker_key = Column(String())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
