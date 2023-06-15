"""empty message

Revision ID: 0d427d2897b5
Revises: 97cac1c6ef1a
Create Date: 2023-06-15 23:41:32.512205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d427d2897b5'
down_revision = '97cac1c6ef1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('venue_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'venues', ['venue_id'], ['id'])

    with op.batch_alter_table('venue_artist', schema=None) as batch_op:
        batch_op.drop_constraint('venue_artist_event_id_fkey', type_='foreignkey')
        batch_op.drop_column('event_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('venue_artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('venue_artist_event_id_fkey', 'event', ['event_id'], ['id'])

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('venue_id')

    # ### end Alembic commands ###