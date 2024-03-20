"""rental model update

Revision ID: 8a35b902d92d
Revises: a6e0b6c35e12
Create Date: 2024-03-19 07:32:41.480978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a35b902d92d'
down_revision = 'a6e0b6c35e12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rental', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('access_duration', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('approval_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('book_count', sa.Integer(), nullable=False))
        batch_op.alter_column('date_issued',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column('return_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rental', schema=None) as batch_op:
        batch_op.alter_column('return_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('date_issued',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
        batch_op.drop_column('book_count')
        batch_op.drop_column('approval_time')
        batch_op.drop_column('access_duration')
        batch_op.drop_column('approved')

    # ### end Alembic commands ###