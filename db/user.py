from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class User(Base):
    __tablename__ = 'users'
