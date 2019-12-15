from .base import Base
from sqlalchemy import Integer, String, DateTime, JSON, Column


class PivotCandidate(Base):
    __tablename__ = 'pivot_candidates'
    id = Column(Integer(), primary_key=True)
    uri = Column(String(), nullable=False)
    analyzed = Column(JSON())
    transaction_key = Column(String())
    taker_key = Column(String())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
