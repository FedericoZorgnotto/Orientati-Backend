"""aggiunti log gruppi-tappe

Revision ID: 48d8b21a95be
Revises: 2c8ee1b8efb7
Create Date: 2025-06-07 08:16:53.534831

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '48d8b21a95be'
down_revision: Union[str, None] = '2c8ee1b8efb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('LogGruppiTappe',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('gruppo_id', sa.Integer(), nullable=False),
                    sa.Column('tappa_id', sa.Integer(), nullable=False),
                    sa.Column('timestamp', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    with op.batch_alter_table('Gruppi') as batch_op:
        batch_op.alter_column('fasciaOraria_id',
                              existing_type=sa.INTEGER(),
                              nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table('Gruppi') as batch_op:
        batch_op.alter_column('fasciaOraria_id',
                              existing_type=sa.INTEGER(),
                              nullable=True)

    op.drop_table('LogGruppiTappe')
    # ### end Alembic commands ###
