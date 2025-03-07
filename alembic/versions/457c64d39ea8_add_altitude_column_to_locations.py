"""Add altitude column to locations

Revision ID: 457c64d39ea8
Revises:
Create Date: 2023-09-23 11:04:53.375587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457c64d39ea8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('locations', sa.Column(
      'altitude', sa.Float(), nullable=False, server_default='0.0'))


def downgrade():
  op.drop_column('locations', 'altitude')
