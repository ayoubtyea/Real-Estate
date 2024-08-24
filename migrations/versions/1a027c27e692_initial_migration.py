"""Initial migration

Revision ID: 1a027c27e692
Revises: 
Create Date: 2024-08-24 00:00:34.922600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a027c27e692'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('request', schema=None) as batch_op:
        batch_op.alter_column('payment_id',
               existing_type=sa.VARCHAR(length=1000),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('request', schema=None) as batch_op:
        batch_op.alter_column('payment_id',
               existing_type=sa.VARCHAR(length=1000),
               nullable=False)

    # ### end Alembic commands ###
