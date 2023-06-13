"""empty message

Revision ID: 19ec22a14b4c
Revises: 500d227f5d8f
Create Date: 2023-06-13 16:08:47.985586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19ec22a14b4c'
down_revision = '500d227f5d8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('artist_genre',
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artist_genre')
    op.drop_table('venues')
    op.drop_table('genres')
    op.drop_table('artists')
    # ### end Alembic commands ###
