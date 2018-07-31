"""empty message

Revision ID: 74b2a0989d26
Revises: e4923ce4b117
Create Date: 2017-02-15 16:30:42.836000

"""

# revision identifiers, used by Alembic.
revision = '74b2a0989d26'
down_revision = 'e4923ce4b117'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_esg_summary',
    sa.Column('company_id', sa.String(length=20), nullable=False),
    sa.Column('data_provider_id', sa.String(length=20), nullable=False),
    sa.Column('esg_score', sa.Float(), nullable=True),
    sa.Column('revenue', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['data_provider_id'], ['data_provider.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'data_provider_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_esg_summary')
    # ### end Alembic commands ###