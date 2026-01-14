"""books: replace file_path with file_id

Revision ID: 21768e6a9349
Revises: 0ac5706dd1de
Create Date: 2025-12-31 15:36:15.593356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21768e6a9349'
down_revision: Union[str, Sequence[str], None] = '0ac5706dd1de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema"""
    with op.batch_alter_table("books") as batch:
        # 1) add books.file_id
        batch.add_column(sa.Column("file_id", sa.String(), nullable=True))

        # 2) FK: books.file_id -> files.id
        batch.create_foreign_key(
            "fk_books_file_id_files",
            "files",
            ["file_id"],
            ["id"],
            ondelete="SET NULL",
        )

        # 3) drop old column
        batch.drop_column("file_path")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("books") as batch:
        # 1) restore old column
        batch.add_column(sa.Column("file_path", sa.String(), nullable=True))

        # 2) drop FK + file_id
        batch.drop_constraint("fk_books_file_id_files", type_="foreignkey")
        batch.drop_column("file_id")
