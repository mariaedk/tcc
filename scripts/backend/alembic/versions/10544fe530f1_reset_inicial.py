"""reset inicial

Revision ID: 10544fe530f1
Revises:
Create Date: 2025-05-01 13:42:42.432013

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = '10544fe530f1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'usuario',
        sa.Column('id_usuario', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ds_nome', sa.String(255), nullable=False),
        sa.Column('ds_username', sa.String(100), nullable=False),
        sa.Column('ds_email', sa.String(255), nullable=False),
        sa.Column('ds_senha', sa.String(400), nullable=False),
        sa.Column('tp_usuario', sa.String(50), nullable=False),
        sa.PrimaryKeyConstraint('id_usuario'),
        sa.UniqueConstraint('ds_username'),
        sa.UniqueConstraint('ds_email'),
    )

    op.create_table(
        'dispositivo',
        sa.Column('id_dispositivo', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ds_nome', sa.String(255), nullable=False),
        sa.Column('cd_dispositivo', sa.BigInteger(), nullable=True),
        sa.Column('tp_dispositivo', sa.String(50), nullable=False),
        sa.Column('ds_localizacao', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id_dispositivo'),
        sa.UniqueConstraint('cd_dispositivo'),
    )

    op.create_table(
        'sensor',
        sa.Column('id_sensor', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ds_nome', sa.String(255), nullable=False),
        sa.Column('cd_sensor', sa.BigInteger(), nullable=True),
        sa.Column('tp_sensor', sa.String(50), nullable=False),
        sa.Column('dispositivo_id_dispositivo', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['dispositivo_id_dispositivo'], ['dispositivo.id_dispositivo']),
        sa.PrimaryKeyConstraint('id_sensor'),
        sa.UniqueConstraint('cd_sensor'),
    )

    op.create_table(
        'unidade_medida',
        sa.Column('id_unidade_medida', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ds_denominacao', sa.String(50), nullable=False),
        sa.Column('ds_sigla', sa.String(10), nullable=False),
        sa.PrimaryKeyConstraint('id_unidade_medida'),
    )

    op.create_table(
        'coleta',
        sa.Column('id_coleta', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('dt_hora', sa.DateTime(), nullable=True),
        sa.Column('origem', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id_coleta'),
    )

    op.create_table(
        'medicao',
        sa.Column('id_medicao', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('coleta_id_coleta', sa.BigInteger(), nullable=False),
        sa.Column('sensor_id_sensor', sa.BigInteger(), nullable=False),
        sa.Column('unidade_medida_id_unidade_medida', sa.BigInteger(), nullable=False),
        sa.Column('vl_valor', sa.Float(), nullable=True),
        sa.Column('vl_valor_str', sa.String(255), nullable=True),
        sa.Column('vl_valor_bool', sa.Boolean(), nullable=True),
        sa.Column('dt_hora', sa.DateTime(), nullable=False),
        sa.Column('tp_tipo', sa.String(50), nullable=False),
        sa.Column('fl_falha', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['coleta_id_coleta'], ['coleta.id_coleta']),
        sa.ForeignKeyConstraint(['sensor_id_sensor'], ['sensor.id_sensor']),
        sa.ForeignKeyConstraint(['unidade_medida_id_unidade_medida'], ['unidade_medida.id_unidade_medida']),
        sa.PrimaryKeyConstraint('id_medicao', 'dt_hora'),
    )


def downgrade() -> None:
    op.drop_table('medicao')
    op.drop_table('coleta')
    op.drop_table('unidade_medida')
    op.drop_table('sensor')
    op.drop_table('dispositivo')
    op.drop_table('usuario')
