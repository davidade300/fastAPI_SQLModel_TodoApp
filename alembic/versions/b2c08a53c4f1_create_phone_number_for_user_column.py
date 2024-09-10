"""Create phone number for user column

Revision ID: b2c08a53c4f1
Revises:
Create Date: 2024-09-09 21:50:39.632668

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c08a53c4f1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        table_name="users",
        column=sa.Column(
            "phone_number", sa.String(), nullable=True, unique=True
        ),
    )


def downgrade() -> None:
    op.drop_column(table_name="users", column_name="phone_number")
