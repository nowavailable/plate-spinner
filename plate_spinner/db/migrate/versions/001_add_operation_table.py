from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import SMALLINT, BIGINT, VARCHAR, DATETIME, BLOB, TEXT, TINYINT, JSON
from migrate.changeset.constraint import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.schema import Index

meta = MetaData()

jobqueue_table = Table(
    "ps_jobqueues", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("job_name", VARCHAR(255), nullable=True),
    # Column("job_type", SMALLINT(unsigned=True), nullable=False, default=0),
    Column("parameters", JSON, nullable=True),
    Column("sharding_keystr", VARCHAR(255), nullable=True),
    Column("ready_at", DATETIME, nullable=False),
    Column("taken_at", DATETIME, nullable=True),
    Column("taken_cont", SMALLINT(unsigned=True), nullable=False, default=0),
    Column("finished_at", DATETIME, nullable=True),
    #Column("return_value", JSON, nullable=True),
    Column("created_at", DATETIME, nullable=False)
)
jobqueue_index_1 = Index(
    "idx_ps_jobqueues_keystr",
    jobqueue_table.c.job_name,
    jobqueue_table.c.sharding_keystr,
    jobqueue_table.c.ready_at,
    jobqueue_table.c.taken_at,
    unique=False
)
jobqueue_index_2 = Index(
    "idx_ps_jobqueues_finished",
    jobqueue_table.c.finished_at,
    unique=False
)

# root_process_table = Table()

# operation_table = Table(
#     "ps_operations", meta,
#     Column("id", BIGINT(unsigned=True), primary_key=True),
#     Column("keystr", VARCHAR(255), nullable=False),
#     Column("started_at", DATETIME, nullable=False),
#     Column("finished_at", DATETIME, nullable=False),
#     Column("emergency", TINYINT, nullable=False, default=0),
#     Column("interval_of_job", SMALLINT(unsigned=True), nullable=False, default=0),
#     Column("limit_of_job", SMALLINT(unsigned=True), nullable=False, default=0),
#     # Column("jobname_will_generate", VARCHAR(255), nullable=True),
#     Column("jobname", VARCHAR(255), nullable=False),
#     Column("next_keystr", VARCHAR(255), nullable=True),
#     Column("created_at", DATETIME, nullable=False),
#     Column("updated_at", DATETIME, nullable=False),
# )
# operation_index_1 = Index(
#     "idx_ps_operations_keystr",
#     operation_table.c.keystr,
#     unique=False
# )
# schedule_table = Table(
#     "ps_schedules", meta,
#     Column("id", BIGINT(unsigned=True), primary_key=True),
#     Column("operation_id", BIGINT(unsigned=True), nullable=False),
#     Column("object_identity", JSON, nullable=False),
#     Column("sharding_keystr", VARCHAR(255), nullable=True),
#     Column("started_at", DATETIME, nullable=False),
#     Column("finished_at", DATETIME, nullable=False),
#     Column("parameters", JSON, nullable=True),
#     Column("return_value", JSON, nullable=True),
#     Column("created_at", DATETIME, nullable=False),
#     Column("updated_at", DATETIME, nullable=False),
# )
# fkey_schedule_table = ForeignKeyConstraint(
#     [schedule_table.c.operation_id], [operation_table.c.id]
# )
# schedule_index_1 = Index(
#     "idx_ps_schedules_sharding_keystr",
#     schedule_table.c.operation_id, schedule_table.c.sharding_keystr,
#     unique=False
# )
# looped_operation_table = Table(
#     "ps_looped_operations", meta,
#     Column("id", BIGINT(unsigned=True), primary_key=True),
#     Column("start", TINYINT, nullable=False, default=1),
#     Column("stop", TINYINT, nullable=False, default=0),
#     Column("previous_state", JSON, nullable=True),
#     Column("jobname", VARCHAR(255), nullable=False),
#     Column("jobname_next", VARCHAR(255), nullable=True),
#     Column("generated_jobname_next", VARCHAR(255), nullable=True),
#     Column("created_at", DATETIME, nullable=False),
#     Column("updated_at", DATETIME, nullable=False)
# )
# generated_job_table = Table(
#     "ps_generated_jobs", meta,
#     Column("id", BIGINT(unsigned=True), primary_key=True),
#     Column("jobname", VARCHAR(255), nullable=False),
#     Column("operation_id", BIGINT(unsigned=True), nullable=False),
#     Column("started_at", DATETIME, nullable=False),
#     Column("finished_at", DATETIME, nullable=False),
#     Column("created_at", DATETIME, nullable=False),
#     Column("updated_at", DATETIME, nullable=False),
# )
# fkey_generated_job_table = ForeignKeyConstraint(
#     [generated_job_table.c.operation_id], [operation_table.c.id]
# )

def upgrade(migrate_engine):
    meta.bind = migrate_engine

    jobqueue_table.create()

    # operation_table.create()
    # schedule_table.create()
    # fkey_schedule_table.create()
    # looped_operation_table.create()
    # generated_job_table.create()
    # fkey_generated_job_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    jobqueue_table.drop()

    # generated_job_table.drop()
    # looped_operation_table.drop()
    # schedule_table.drop()
    # operation_table.drop()
