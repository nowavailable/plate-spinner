from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class EpisodeCandidate(Base):
    __tablename__ = 'episode_candidates'
