from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class Episode(Base):
    __tablename__ = 'episodes'
