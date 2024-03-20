"""create_user_table

Revision ID: 2e5ba5ba0672
Revises: 
Create Date: <timestamp>

"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '2e5ba5ba0672'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'User',
        sa.Column('uid', sa.String(length=36), primary_key=True),
        sa.Column('username', sa.String(length=20), nullable=False, unique=True),
        sa.Column('password', sa.String(length=200), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('User')

