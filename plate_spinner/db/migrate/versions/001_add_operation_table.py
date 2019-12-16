from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import SMALLINT, BIGINT, VARCHAR, DATETIME, BLOB, TEXT, TINYINT, JSON
from migrate.changeset.constraint import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.schema import Index

meta = MetaData()

jobqueue_sun_table = Table(
    "ps_jobqueue_suns", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("job_name", VARCHAR(255), nullable=False),
    # Column("job_type", SMALLINT(unsigned=True), nullable=False, default=0),
    Column("parameters", JSON, nullable=True),
    Column("sharding_keystr", VARCHAR(255), nullable=True),
    Column("ready_at", DATETIME, nullable=False),
    Column("finished_at", DATETIME, nullable=True),
    #Column("return_value", JSON, nullable=True),
    Column("created_at", DATETIME, nullable=False)
)
jobqueue_sun_index_1 = Index(
    "idx_ps_jobqueue_suns_keystr",
    jobqueue_sun_table.c.job_name,
    jobqueue_sun_table.c.sharding_keystr,
    jobqueue_sun_table.c.ready_at,
    unique=False
)
jobqueue_sun_index_2 = Index(
    "idx_ps_jobqueue_suns_finished",
    jobqueue_sun_table.c.finished_at,
    unique=False
)

job_taken_sun_table = Table(
    "ps_job_taken_suns", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("ps_jobqueue_sun_id", BIGINT(unsigned=True), nullable=False),
    Column("created_at", DATETIME, nullable=False)
)
fkey_job_taken_sun_table = ForeignKeyConstraint(
    [job_taken_sun_table.c.ps_jobqueue_sun_id], [jobqueue_sun_table.c.id]
)
job_taken_sun_index_1 = Index(
    "idx_ps_job_taken_suns_ps_jobqueue_sun_id",
    job_taken_sun_table.c.ps_jobqueue_sun_id,
    unique=True
)

jobqueue_moon_table = Table(
    "ps_jobqueue_moons", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("job_name", VARCHAR(255), nullable=False),
    # Column("job_type", SMALLINT(unsigned=True), nullable=False, default=0),
    Column("parameters", JSON, nullable=True),
    Column("sharding_keystr", VARCHAR(255), nullable=True),
    Column("ready_at", DATETIME, nullable=False),
    Column("finished_at", DATETIME, nullable=True),
    Column("created_at", DATETIME, nullable=False)
)
jobqueue_moon_index_1 = Index(
    "idx_ps_jobqueue_moons_keystr",
    jobqueue_moon_table.c.job_name,
    jobqueue_moon_table.c.sharding_keystr,
    jobqueue_moon_table.c.ready_at,
    unique=False
)
jobqueue_moon_index_2 = Index(
    "idx_ps_jobqueue_moons_finished",
    jobqueue_moon_table.c.finished_at,
    unique=False
)

job_taken_moon_table = Table(
    "ps_job_taken_moons", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("ps_jobqueue_moon_id", BIGINT(unsigned=True), nullable=False),
    Column("created_at", DATETIME, nullable=False)
)
fkey_job_taken_moon_table = ForeignKeyConstraint(
    [job_taken_moon_table.c.ps_jobqueue_moon_id], [jobqueue_moon_table.c.id]
)
job_taken_moon_index_1 = Index(
    "idx_ps_job_taken_moons_ps_jobqueue_moon_id",
    job_taken_moon_table.c.ps_jobqueue_moon_id,
    unique=True
)


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

    jobqueue_sun_table.create()
    job_taken_sun_table.create()
    fkey_job_taken_sun_table.create()

    jobqueue_moon_table.create()
    job_taken_moon_table.create()
    fkey_job_taken_moon_table.create()

    # operation_table.create()
    # schedule_table.create()
    # fkey_schedule_table.create()
    # looped_operation_table.create()
    # generated_job_table.create()
    # fkey_generated_job_table.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    job_taken_moon_table.drop()
    jobqueue_moon_table.drop()

    job_taken_sun_table.drop()
    jobqueue_sun_table.drop()

    # generated_job_table.drop()
    # looped_operation_table.drop()
    # schedule_table.drop()
    # operation_table.drop()

