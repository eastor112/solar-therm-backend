"""Adding missing param to TheoricParams model

Revision ID: e8d5ca6f13c1
Revises: 69fb5ed17ad6
Create Date: 2023-09-23 14:31:50.970790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8d5ca6f13c1'
down_revision = '69fb5ed17ad6'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('theoric_params', sa.Column('pipeline_separation',
                sa.Float(), nullable=True, server_default='0.0'))


def downgrade():
  op.drop_column('theoric_params', 'pipeline_separation')
