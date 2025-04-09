"""parametri genitore nullable

Revision ID: a47239208574
Revises: 00833ed21e0e
Create Date: 2025-04-09 09:06:50.604747

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a47239208574'
down_revision: Union[str, None] = '00833ed21e0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Creare tabella temporanea
    with op.batch_alter_table('Genitori') as batch_op:
        batch_op.alter_column('nome',
                            existing_type=sa.String(),
                            nullable=True)
        batch_op.alter_column('cognome',
                            existing_type=sa.String(),
                            nullable=True)
        batch_op.alter_column('comune',
                            existing_type=sa.String(),
                            nullable=True)


def downgrade() -> None:
    with op.batch_alter_table('Genitori') as batch_op:
        batch_op.alter_column('nome',
                            existing_type=sa.String(),
                            nullable=False)
        batch_op.alter_column('cognome',
                            existing_type=sa.String(),
                            nullable=False)
        batch_op.alter_column('comune',
                            existing_type=sa.String(),
                            nullable=False)
