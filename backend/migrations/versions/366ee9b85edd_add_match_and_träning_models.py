"""Add match and träning models

Revision ID: 366ee9b85edd
Revises: cf37253ccb59
Create Date: 2025-03-22 00:53:18.483866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '366ee9b85edd'
down_revision = 'cf37253ccb59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_lag', schema=None) as batch_op:
        batch_op.add_column(sa.Column('skapad_datum', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_lag', schema=None) as batch_op:
        batch_op.drop_column('skapad_datum')

    # ### end Alembic commands ###
