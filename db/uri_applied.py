from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class UriApplied(Base):
    __tablename__ = 'uri_applieds'
