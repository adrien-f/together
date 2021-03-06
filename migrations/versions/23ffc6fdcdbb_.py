"""empty message

Revision ID: 23ffc6fdcdbb
Revises: 1e0032f4e675
Create Date: 2014-06-08 22:19:31.192208

"""

# revision identifiers, used by Alembic.
revision = '23ffc6fdcdbb'
down_revision = '1e0032f4e675'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'user', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user')
    op.drop_table('playlist')
    ### end Alembic commands ###
