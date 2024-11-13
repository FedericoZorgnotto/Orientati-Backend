"""aggiunta relazione utente orientatore

Revision ID: b008400811d1
Revises: 992a670c5df1
Create Date: 2024-11-13 09:26:02.743867

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Inspector

# revision identifiers, used by Alembic.
revision: str = 'b008400811d1'
down_revision: Union[str, None] = '992a670c5df1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Get the current connection
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)

    # Check if the column already exists
    columns = [col['name'] for col in inspector.get_columns('Utenti')]
    if 'orientatore_id' not in columns:
        op.add_column('Utenti', sa.Column('orientatore_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('Utenti') as batch_op:
        batch_op.create_foreign_key("fk_utenti_orientatore_id", 'Orientatori', ['orientatore_id'], ['id'])


def downgrade():
    with op.batch_alter_table('Utenti') as batch_op:
        batch_op.drop_constraint("fk_utenti_orientatore_id", type_='foreignkey')
    op.drop_column('Utenti', 'orientatore_id')
