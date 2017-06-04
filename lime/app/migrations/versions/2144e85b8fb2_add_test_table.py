"""Add test table

Revision ID: 2144e85b8fb2
Revises: f503bc908e65
Create Date: 2017-06-04 10:08:45.886750

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2144e85b8fb2'
down_revision = 'f503bc908e65'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('tests',
    sa.Column('id', mysql.INTEGER(display_width=12)),
    sa.Column('problem_id', mysql.VARCHAR(length=12)),
    sa.Column('input', mysql.BLOB(), nullable=False),
    sa.Column('output', mysql.BLOB(), nullable=False),
    sa.Column('example', mysql.TINYINT(), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
  )


def downgrade():
  op.drop_table('tests')
