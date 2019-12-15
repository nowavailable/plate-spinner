from sqlalchemy import *
from sqlalchemy.dialects.mysql import SMALLINT, BIGINT, VARCHAR, DATETIME, BLOB, TEXT, TINYINT, JSON
from migrate import *


meta = MetaData()

running_table = Table(
    "ps_runnings", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("hostname", VARCHAR(255), nullable=False),
    Column("process_id_str", VARCHAR(255), nullable=False),
    Column("emergency", BOOLEAN, nullable=False, default=False),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)

mode_table = Table(
    "ps_modes", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("mode", VARCHAR(255), nullable=False)
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    running_table.create()
    mode_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    mode_table.drop()
    running_table.drop()
