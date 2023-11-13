"""add_project_id_to_params

Revision ID: 8f88dcaf52be
Revises: c948714912dd
Create Date: 2023-11-12 19:49:25.495347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f88dcaf52be'
down_revision = 'c948714912dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.add_column('theoric_params', sa.Column(
      'project_id', sa.Integer(), nullable=True))
  op.create_foreign_key(None, 'theoric_params',
                        'projects', ['project_id'], ['id'])
  # ### end Alembic commands ###


def downgrade() -> None:
  op.drop_constraint(None, 'theoric_params', type_='foreignkey')
  op.drop_column('theoric_params', 'project_id')
