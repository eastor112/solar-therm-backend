"""Rename long to length in pipeline type

Revision ID: 69fb5ed17ad6
Revises: bb0ecfd9a34e
Create Date: 2023-09-23 12:13:15.303159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69fb5ed17ad6'
down_revision = 'bb0ecfd9a34e'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column('pipelines', 'long', new_column_name='length')


def downgrade():
  op.alter_column('pipelines', 'length', new_column_name='long')
