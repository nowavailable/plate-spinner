from sqlalchemy.ext.automap import automap_base
Base = automap_base()


class SerialStory(Base):
    __tablename__ = 'serial_stories'

