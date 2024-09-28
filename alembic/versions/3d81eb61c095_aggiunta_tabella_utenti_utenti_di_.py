"""Aggiunta tabella utenti + utenti di esempio

Revision ID: 3d81eb61c095
Revises: 
Create Date: 2024-09-28 12:27:45.187716

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d81eb61c095'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #riporto per comodità il modello utente:
    #class User(Base):
    # __tablename__ = "users"
    # id = Column(Integer, primary_key=True, index=True)
    # username = Column(String, unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # hashed_password = Column(String)
    # is_admin = Column(Boolean, default=False)



    #creo la tabella utenti
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_admin", sa.Boolean, default=False)
    )

    #inserisco due utenti di esempio
    op.execute(
        """
        INSERT INTO users (username, email, hashed_password, is_admin)
        VALUES ('admin', 'admin@admin.com', '8C6976E5B5410415BDE908BD4DEE15DFB167A9C873FC4BB8A81F6F2AB448A918', true)
        """
    ) #password: admin

    op.execute(
        """
        INSERT INTO users (username, email, hashed_password, is_admin)
        VALUES ('user', 'user@user.com', '04F8996DA763B7A969B1028EE3007569EAF3A635486DDAB211D512C85B9DF8FB', False) 
        """
    ) #password: user




def downgrade() -> None:

    #elimino la tabella utenti
    op.drop_table("users")