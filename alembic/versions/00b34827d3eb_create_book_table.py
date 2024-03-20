"""create_book_table

Revision ID: 00b34827d3eb
Revises: 
Create Date: <timestamp>

"""

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = "00b34827d3eb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "Book",
        sa.Column(
            "uid",
            sa.String(length=36),
            primary_key=True,
            default=lambda: str(uuid.uuid4()),
        ),
        sa.Column("title", sa.String(length=200), nullable=False, unique=True),
        sa.Column("available", sa.String(length=200)),
        sa.Column("file_path", sa.String(length=255)),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True,
            server_default=sa.func.now(),
        ),
    )


def downgrade():
    op.drop_table("Book")
