"""init

Revision ID: 236519173da5
Revises: 
Create Date: 2023-01-16 01:38:24.455049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '236519173da5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'menu_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('price', sa.Integer, nullable=False)
    )


def downgrade():
    op.drop_table('menu_items')
