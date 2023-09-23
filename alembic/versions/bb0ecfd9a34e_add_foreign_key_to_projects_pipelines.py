"""Add foreign key to projects pipelines

Revision ID: bb0ecfd9a34e
Revises: f2a4b74af80f
Create Date: 2023-09-23 11:50:45.143023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb0ecfd9a34e'
down_revision = 'f2a4b74af80f'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('projects', sa.Column(
      'pipeline_id', sa.Integer(), nullable=True))
  op.create_foreign_key('fk_project_pipeline', 'projects',
                        'pipelines', ['pipeline_id'], ['id'])


def downgrade():
  op.drop_constraint('fk_project_pipeline', 'projects', type_='foreignkey')
  op.drop_column('projects', 'pipeline_id')
