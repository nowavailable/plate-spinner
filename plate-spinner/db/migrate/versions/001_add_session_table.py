from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, BLOB, TEXT, TINYINT, JSON
from migrate.changeset.constraint import ForeignKeyConstraint


meta = MetaData()
session_table = Table(
    "ps_sessions", meta,
    Column('id', BIGINT(unsigned=True), primary_key=True),
    Column('started_at', DATETIME, nullable=False),
    Column('finished_at', DATETIME, nullable=False),
    Column('emergency', TINYINT, nullable=False, default=0),
    Column('interval_of_job', BIGINT(unsigned=True), nullable=False, default=0),
    Column('limit_of_job', BIGINT(unsigned=True), nullable=False, default=0),
    Column('jobname_will_generate', VARCHAR(255), nullable=True),
    Column('created_at', DATETIME, nullable=False),
    Column('updated_at', DATETIME, nullable=False)
)
schedule_table = Table(
    "ps_schedules", meta,
    Column('id', BIGINT(unsigned=True), primary_key=True),
    Column('session_id', BIGINT(unsigned=True), nullable=False),
    Column('object_identity', JSON, nullable=False),
    Column('started_at', DATETIME, nullable=False),
    Column('finished_at', DATETIME, nullable=False),
    Column('parameters', JSON, nullable=True),
    Column('return_value', JSON, nullable=True),
    Column('created_at', DATETIME, nullable=False),
    Column('updated_at', DATETIME, nullable=False)
)
fkey_schedule_table = ForeignKeyConstraint(
    [schedule_table.c.session_id], [session_table.c.id]
)
looped_session_table = Table(
    "ps_looped_sessions", meta,
    Column('id', BIGINT(unsigned=True), primary_key=True),
    Column('start', TINYINT, nullable=False, default=1),
    Column('stop', TINYINT, nullable=False, default=0),
    Column('previous_state', JSON, nullable=True),
    Column('jobname', VARCHAR(255), nullable=False),
    Column('jobname_next', VARCHAR(255), nullable=True),
    Column('generated_jobname_next', VARCHAR(255), nullable=True),
    Column('created_at', DATETIME, nullable=False),
    Column('updated_at', DATETIME, nullable=False)
)
generated_job_table = Table(
    "ps_generated_jobs", meta,
    Column('id', BIGINT(unsigned=True), primary_key=True),
    Column('jobname', VARCHAR(255), nullable=False),
    Column('session_id', BIGINT(unsigned=True), nullable=False),
    Column('started_at', DATETIME, nullable=False),
    Column('finished_at', DATETIME, nullable=False),
    Column('created_at', DATETIME, nullable=False),
    Column('updated_at', DATETIME, nullable=False)
)
fkey_generated_job_table = ForeignKeyConstraint(
    [generated_job_table.c.session_id], [session_table.c.id]
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    session_table.create()
    schedule_table.create()
    fkey_schedule_table.create()
    looped_session_table.create()
    generated_job_table.create()
    fkey_generated_job_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    generated_job_table.drop()
    looped_session_table.drop()
    schedule_table.drop()
    session_table.drop()
