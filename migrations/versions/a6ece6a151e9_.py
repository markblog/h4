"""empty message

Revision ID: a6ece6a151e9
Revises: a79b5c20fcb3
Create Date: 2017-01-24 18:20:40.729032

"""

# revision identifiers, used by Alembic.
revision = 'a6ece6a151e9'
down_revision = 'a79b5c20fcb3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('geography',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(200), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['geography.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('data_provider',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('esg_rating',
    sa.Column('id', sa.String(length=5), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('geography_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['geography_id'], ['geography.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('esg_factor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('data_provider_id', sa.String(length=20), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['data_provider_id'], ['data_provider.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['esg_factor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('geography_financial_series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('geography_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('revenue', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['geography_id'], ['geography.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_esg_factor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.String(length=20), nullable=True),
    sa.Column('esg_factor_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['esg_factor_id'], ['esg_factor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_esg_series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.String(length=20), nullable=True),
    sa.Column('data_provider_id', sa.String(length=20), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('rating', sa.String(length=5), nullable=True),
    sa.Column('e_score', sa.Float(), nullable=True),
    sa.Column('s_score', sa.Float(), nullable=True),
    sa.Column('g_score', sa.Float(), nullable=True),
    sa.Column('total_score', sa.Float(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['data_provider_id'], ['data_provider.id'], ),
    sa.ForeignKeyConstraint(['rating'], ['esg_rating.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_financial_series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.String(length=20), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('closing_price', sa.Float(), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('company_supplier',
    sa.Column('company_id', sa.String(length=20), nullable=False),
    sa.Column('supplier_id', sa.String(length=20), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['company.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['company.id'], ),
    sa.PrimaryKeyConstraint('company_id', 'supplier_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('company_supplier')
    op.drop_table('company_financial_series')
    op.drop_table('company_esg_series')
    op.drop_table('company_esg_factor')
    op.drop_table('geography_financial_series')
    op.drop_table('esg_factor')
    op.drop_table('company')
    op.drop_table('esg_rating')
    op.drop_table('data_provider')
    # ### end Alembic commands ###
