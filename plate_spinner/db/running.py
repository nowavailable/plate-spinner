from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class Running(Base):
    __tablename__ = 'pr_runnings'
