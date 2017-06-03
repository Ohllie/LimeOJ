"""Add users table

Revision ID: 318d01fd68de
Revises:
Create Date: 2017-05-20 15:54:00.592704

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '318d01fd68de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('users',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),

    sa.Column('username', mysql.VARCHAR(length=16), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=256), nullable=False),

    sa.Column('created_at', mysql.INTEGER(display_width=11), nullable=True),
    sa.Column('last_login', mysql.INTEGER(display_width=11), nullable=True),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username'),

    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
  )


def downgrade():
  op.drop_table('users')
