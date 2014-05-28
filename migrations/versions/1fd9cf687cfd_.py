"""empty message

Revision ID: 1fd9cf687cfd
Revises: None
Create Date: 2014-05-27 21:18:40.553014

"""

# revision identifiers, used by Alembic.
revision = '1fd9cf687cfd'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=110), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('pwdhash', sa.String(length=54), nullable=True),
    sa.Column('lastseen', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    ### end Alembic commands ###
