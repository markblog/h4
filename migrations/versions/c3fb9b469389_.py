"""empty message

Revision ID: c3fb9b469389
Revises: 5bef031772b0
Create Date: 2017-02-17 11:22:30.011000

"""

# revision identifiers, used by Alembic.
revision = 'c3fb9b469389'
down_revision = '5bef031772b0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_esg_series', sa.Column('rating_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('company_esg_series', 'rating_date')
    # ### end Alembic commands ###