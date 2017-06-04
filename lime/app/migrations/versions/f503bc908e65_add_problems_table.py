"""Add problems table

Revision ID: f503bc908e65
Revises: 1510789a8f32
Create Date: 2017-06-03 22:12:41.411058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f503bc908e65'
down_revision = '1510789a8f32'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('problems',
    sa.Column('id', mysql.VARCHAR(length=12)),
    sa.Column('title', mysql.VARCHAR(length=64)),
    sa.Column('description', mysql.TEXT()),
    sa.Column('difficulty', mysql.ENUM("1", "2", "3", "4", "5"), nullable=False),
    sa.Column('grader', mysql.TEXT(), nullable=False),

    sa.Column('time_limit', mysql.DOUBLE(), nullable=False),
    sa.Column('memory_limit', mysql.INTEGER(display_width=12), nullable=False),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title'),

    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
  )


def downgrade():
  op.drop_table('problems')
