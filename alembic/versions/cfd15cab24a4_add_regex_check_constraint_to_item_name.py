"""Add regex check constraint to item name

Revision ID: cfd15cab24a4
Revises: 3585d1059e4a
Create Date: 2026-01-03 11:35:35.375257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'cfd15cab24a4'
down_revision: Union[str, Sequence[str], None] = '3585d1059e4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Regex: Alphanumeric (English/Korean) and spaces only.
    # Postgres regex operator is '~'
    op.create_check_constraint(
        "check_item_name_regex",
        "item",
        "name ~ '^[a-zA-Z0-9가-힣 ]+$'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("check_item_name_regex", "item", type_="check")
