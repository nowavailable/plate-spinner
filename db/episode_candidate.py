from .base import Base
from sqlalchemy import Integer, String, DateTime, Text, JSON, Column, ForeignKey
from sqlalchemy.orm import relationship


class EpisodeCandidate(Base):
    __tablename__ = 'episode_candidates'
    id = Column(Integer(), primary_key=True)
    pivot_candidate_id = Column(Integer(), ForeignKey("pivot_candidates.id"))
    pivot_candidate = relationship("PivotCandidate")

    uri = Column(String(), nullable=False)
    analyzed = Column(JSON())
    content = Column(Text())
    transaction_key = Column(String())
    taker_key = Column(String())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
