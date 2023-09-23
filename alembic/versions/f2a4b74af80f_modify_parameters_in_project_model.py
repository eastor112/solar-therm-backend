"""Modify parameters in project model

Revision ID: f2a4b74af80f
Revises: 457c64d39ea8
Create Date: 2023-09-23 11:14:17.820318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2a4b74af80f'
down_revision = '457c64d39ea8'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('projects', sa.Column('pipeline_separation',
                sa.Float(), nullable=True, server_default='0.0'))
  op.add_column('projects', sa.Column('inclination_deg',
                sa.Float(), nullable=True, server_default='0.0'))
  op.add_column('projects', sa.Column(
      'azimuth_deg', sa.Float(), nullable=True, server_default='0.0'))
  op.add_column('projects', sa.Column(
      'granularity', sa.Integer(), nullable=True, server_default='0'))

  op.drop_column('projects', 'pipeline_type')


def downgrade():
  op.drop_column('projects', 'pipeline_separation')
  op.drop_column('projects', 'inclination_deg')
  op.drop_column('projects', 'azimuth_deg')
  op.drop_column('projects', 'granularity')

  op.add_column('projects', sa.Column('pipeline_type',
                sa.Integer(), nullable=True, server_default='0'))
