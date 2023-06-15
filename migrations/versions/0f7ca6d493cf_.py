"""empty message

Revision ID: 0f7ca6d493cf
Revises: 971f30fc268f
Create Date: 2023-06-14 01:42:55.639303

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0f7ca6d493cf'
down_revision = '971f30fc268f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('venue_artist', schema=None) as batch_op:
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue_artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))

    op.drop_table('event')
    # ### end Alembic commands ###