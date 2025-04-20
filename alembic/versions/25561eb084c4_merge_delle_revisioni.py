"""Merge delle revisioni

Revision ID: 25561eb084c4
Revises: 9d072dc37758, 7306b1fdc787
Create Date: 2024-12-02 19:48:43.894569

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '25561eb084c4'
down_revision: Union[str, None] = ('9d072dc37758', '7306b1fdc787')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
