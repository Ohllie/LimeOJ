"""Add sessions table

Revision ID: 1510789a8f32
Revises: 318d01fd68de
Create Date: 2017-06-03 19:00:08.071245

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import mysql
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '1510789a8f32'
down_revision = '318d01fd68de'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table('sessions',
    sa.Column('id', mysql.INTEGER(display_width=11)),

    sa.Column('session_id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('data', mysql.BLOB(), nullable=False),
    sa.Column('expiry', mysql.DATETIME(), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('session_id'),
    
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
  )


def downgrade():
  op.drop_table('sessions')
