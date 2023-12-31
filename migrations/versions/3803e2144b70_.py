"""empty message

Revision ID: 3803e2144b70
Revises: de2631edc99d
Create Date: 2023-06-15 23:57:01.979165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3803e2144b70'
down_revision = 'de2631edc99d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('artist_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'artists', ['artist_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('artist_id')

    # ### end Alembic commands ###
