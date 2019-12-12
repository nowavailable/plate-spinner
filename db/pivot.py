from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class Pivot(Base):
    __tablename__ = 'pivots'
