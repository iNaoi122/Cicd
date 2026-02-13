"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-02-13

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE genderenum AS ENUM ('STALLION', 'MARE', 'GELDING')")

    op.create_table(
        "races",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("time", sa.Time(), nullable=False),
        sa.Column("hippodrome", sa.String(200), nullable=False),
        sa.Column("name", sa.String(200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_races_id", "races", ["id"])
    op.create_index("ix_races_date", "races", ["date"])

    op.create_table(
        "owners",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_owners_id", "owners", ["id"])

    op.create_table(
        "jockeys",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("address", sa.String(500), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_jockeys_id", "jockeys", ["id"])

    op.create_table(
        "horses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nickname", sa.String(100), nullable=False),
        sa.Column(
            "gender",
            sa.Enum("STALLION", "MARE", "GELDING", name="genderenum"),
            nullable=False,
        ),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["owners.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_horses_id", "horses", ["id"])

    op.create_table(
        "race_participants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("race_id", sa.Integer(), nullable=False),
        sa.Column("jockey_id", sa.Integer(), nullable=False),
        sa.Column("horse_id", sa.Integer(), nullable=False),
        sa.Column("place", sa.Integer(), nullable=False),
        sa.Column("time_result", sa.Time(), nullable=True),
        sa.ForeignKeyConstraint(["race_id"], ["races.id"]),
        sa.ForeignKeyConstraint(["jockey_id"], ["jockeys.id"]),
        sa.ForeignKeyConstraint(["horse_id"], ["horses.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_race_participants_id", "race_participants", ["id"])
    op.create_index("idx_race_place", "race_participants", ["race_id", "place"])
    op.create_index("idx_jockey_races", "race_participants", ["jockey_id"])
    op.create_index("idx_horse_races", "race_participants", ["horse_id"])


def downgrade() -> None:
    op.drop_table("race_participants")
    op.drop_table("horses")
    op.drop_table("jockeys")
    op.drop_table("owners")
    op.drop_table("races")
    op.execute("DROP TYPE genderenum")
