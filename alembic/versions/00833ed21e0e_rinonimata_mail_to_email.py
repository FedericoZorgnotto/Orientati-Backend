"""rinonimata mail to email

Revision ID: 00833ed21e0e
Revises: 245c6c2fa950
Create Date: 2025-04-09 08:43:22.810001

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '00833ed21e0e'
down_revision: Union[str, None] = '245c6c2fa950'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('Genitori', schema=None) as batch_op:
        batch_op.alter_column('mail',
                              new_column_name='email',
                              existing_type=sa.String(255))


def downgrade() -> None:
    with op.batch_alter_table('Genitori', schema=None) as batch_op:
        batch_op.alter_column('email',
                              new_column_name='mail',
                              existing_type=sa.String(255))
