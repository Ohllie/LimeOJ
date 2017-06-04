"""Add submissions table

Revision ID: 6d7c539c87bc
Revises: 2144e85b8fb2
Create Date: 2017-06-04 14:38:52.020688

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6d7c539c87bc'
down_revision = '2144e85b8fb2'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('submissions',
    sa.Column('id', mysql.INTEGER(display_width=12)),

    sa.Column('problem_id', mysql.VARCHAR(length=12)),
    sa.Column('user_id', mysql.INTEGER(display_width=12)),

    sa.Column('code', mysql.TEXT(), nullable=False),
    sa.Column('language', mysql.VARCHAR(length=12), default='cpp11'),

    sa.Column('status', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('result', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('tests_done', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('tests_total', mysql.INTEGER(display_width=11), nullable=False),

    sa.Column('created_at', mysql.INTEGER(display_width=11)),

    sa.Column('execution_time', mysql.DOUBLE),
    sa.Column('code_length', mysql.INTEGER(display_width=11)),

    sa.PrimaryKeyConstraint('id'),

    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
  )


def downgrade():
  op.drop_table('submissions')
