"""empty message

Revision ID: 22d87ecff971
Revises: 481d94818d45
Create Date: 2014-06-09 05:48:50.820443

"""

# revision identifiers, used by Alembic.
revision = '22d87ecff971'
down_revision = '481d94818d45'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist_element',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('youtube_id', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('added_at', sa.DateTime(), nullable=True),
    sa.Column('added_by_id', sa.Integer(), nullable=True),
    sa.Column('playlist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['added_by_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlist_element')
    ### end Alembic commands ###