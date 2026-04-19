"""timescaledb hypertable

Revision ID: a1b2c3d4e5f6
Revises: 10544fe530f1
Create Date: 2026-04-18 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '10544fe530f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
    op.execute("SELECT create_hypertable('medicao', 'dt_hora');")


def downgrade() -> None:
    pass
