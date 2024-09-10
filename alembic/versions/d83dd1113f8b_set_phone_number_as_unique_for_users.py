"""set phone number  as unique for users

Revision ID: d83dd1113f8b
Revises: b2c08a53c4f1
Create Date: 2024-09-09 22:29:24.063239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd83dd1113f8b'
down_revision: Union[str, None] = 'b2c08a53c4f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
