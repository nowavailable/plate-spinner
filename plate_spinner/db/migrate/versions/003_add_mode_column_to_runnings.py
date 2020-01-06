from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import VARCHAR

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    running_table = Table('ps_runnings', meta, autoload=True)
    mode_column = Column("mode", VARCHAR(255), nullable=False)
    mode_column.create(running_table)


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    running_table = Table('ps_runnings', meta, autoload=True)
    running_table.c.mode.drop()
