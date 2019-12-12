from .mysql import MySQL
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
AutoMap = automap_base()


class JobQueue(AutoMap):
    __tablename__ = "ps_jobqueues"
    # FIXME: 何故かprimary keyがautomapで検出されないので、手動で定義
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

AutoMap.prepare(MySQL.get_engine(), reflect=True)
