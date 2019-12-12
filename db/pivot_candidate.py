from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class PivotCandidate(Base):
    __tablename__ = 'pivot_candidates'
