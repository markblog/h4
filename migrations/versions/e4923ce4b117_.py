"""empty message

Revision ID: e4923ce4b117
Revises: 1dd4af39a4bb
Create Date: 2017-02-13 15:34:11.055000

"""

# revision identifiers, used by Alembic.
revision = 'e4923ce4b117'
down_revision = '1dd4af39a4bb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('esg_factor', sa.Column('esg_type', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('esg_factor', 'esg_type')
    # ### end Alembic commands ###
