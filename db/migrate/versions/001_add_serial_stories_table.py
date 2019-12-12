from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import SMALLINT, BIGINT, VARCHAR, DATETIME, BLOB, TEXT, TINYINT, JSON
from migrate.changeset.constraint import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.schema import Index


meta = MetaData()
user_table = Table(
    "users", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)

uri_applied_table = Table(
    "uri_applieds", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("user_id", BIGINT(unsigned=True), nullable=False),
    Column("uri", VARCHAR(255), nullable=False),
    Column("proc_fixed", TINYINT, nullable=False, default=0),
    Column("proc_count", SMALLINT(unsigned=False), nullable=False, default=0),
    Column("transaction_key", VARCHAR(255), nullable=True),
    Column("taker_key", VARCHAR(255), nullable=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)
fkey_uri_applied_table = ForeignKeyConstraint(
    [uri_applied_table.c.user_id], [user_table.c.id]
)
uri_applied_index_transaction_key = Index(
    "idx_uri_applied_transaction_key",
    uri_applied_table.c.transaction_key,
    unique=False
)
uri_applied_index_1 = Index(
    "idx_uri_applied_uri",
    uri_applied_table.c.uri, uri_applied_table.c.proc_fixed,
    unique=False
)

serial_story_table = Table(
    "serial_stories", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("label", TEXT, nullable=False),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)

pivot_table = Table(
    "pivots", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("serial_story_id", BIGINT(unsigned=True), nullable=False),
    Column("uri", VARCHAR(255), nullable=False),
    Column("analyzed", JSON, nullable=True),
    Column("transaction_key", VARCHAR(255), nullable=True),
    Column("taker_key", VARCHAR(255), nullable=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)
fkey_pivot_table = ForeignKeyConstraint(
    [pivot_table.c.serial_story_id], [serial_story_table.c.id]
)
pivot_index_transaction_key = Index(
    "idx_pivots_transaction_key",
    pivot_table.c.transaction_key,
    unique=False
)
pivot_index_1 = Index(
    "idx_pivots_uri",
    pivot_table.c.uri,
    unique=True
)

episode_table = Table(
    "episodes", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("serial_story_id", BIGINT(unsigned=True), nullable=False),
    Column("number", SMALLINT(unsigned=True), nullable=False, default=1),
    Column("uri", VARCHAR(255), nullable=False),
    Column("analyzed", JSON, nullable=True),
    Column("content", TEXT, nullable=True),
    Column("episode_id", BIGINT(unsigned=True), nullable=True),
    Column("transaction_key", VARCHAR(255), nullable=True),
    Column("taker_key", VARCHAR(255), nullable=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)
fkey_episode_pivot = ForeignKeyConstraint(
    [episode_table.c.serial_story_id], [serial_story_table.c.id]
)
fkey_episode_episode = ForeignKeyConstraint(
    [episode_table.c.episode_id], [episode_table.c.id]
)
episode_index_transaction_key = Index(
    "idx_episodes_transaction_key",
    episode_table.c.transaction_key,
    unique=False
)
episode_index_1 = Index(
    "idx_episodes_uri",
    episode_table.c.uri,
    unique=True
)

pivot_candidate_table = Table(
    "pivot_candidates", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    # Column("serial_story_id", BIGINT(unsigned=True), nullable=False),
    Column("uri", VARCHAR(255), nullable=False),
    Column("analyzed", JSON, nullable=True),
    Column("transaction_key", VARCHAR(255), nullable=True),
    Column("taker_key", VARCHAR(255), nullable=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)
pivot_candidate_index_transaction_key = Index(
    "idx_pivot_cadidates_transaction_key",
    pivot_candidate_table.c.transaction_key,
    unique=False
)

episode_candidate_table = Table(
    "episode_candidates", meta,
    Column("id", BIGINT(unsigned=True), primary_key=True),
    Column("pivot_candidate_id", BIGINT(unsigned=True), nullable=False),
    Column("uri", VARCHAR(255), nullable=False),
    Column("analyzed", JSON, nullable=True),
    Column("content", TEXT, nullable=True),
    Column("transaction_key", VARCHAR(255), nullable=True),
    Column("taker_key", VARCHAR(255), nullable=True),
    Column("created_at", DATETIME, nullable=False),
    Column("updated_at", DATETIME, nullable=False)
)
fkey_episode_candidate_pivot = ForeignKeyConstraint(
    [episode_candidate_table.c.pivot_candidate_id], [pivot_candidate_table.c.id]
)
episode_candidate_index_transaction_key = Index(
    "idx_episode_candidate_transaction_key",
    episode_candidate_table.c.transaction_key,
    unique=False
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine

    user_table.create()
    uri_applied_table.create()
    fkey_uri_applied_table.create()
    serial_story_table.create()
    pivot_table.create()
    fkey_pivot_table.create()
    episode_table.create()
    fkey_episode_pivot.create()
    fkey_episode_episode.create()
    pivot_candidate_table.create()
    episode_candidate_table.create()
    fkey_episode_candidate_pivot.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine

    episode_candidate_table.drop()
    pivot_candidate_table.drop()
    episode_table.drop()
    pivot_table.drop()
    serial_story_table.drop()
    uri_applied_table.drop()
    user_table.drop()

