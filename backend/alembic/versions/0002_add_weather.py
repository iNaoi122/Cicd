"""add weather table

Revision ID: 0002
Revises: 0001
Create Date: 2026-02-13

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("time", sa.Time(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_weather_id", "weather", ["id"])


def downgrade() -> None:
    op.drop_index("ix_weather_id", table_name="weather")
    op.drop_table("weather")
