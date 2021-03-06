"""empty message

Revision ID: a7eae8eb920f
Revises: 00e723b88564
Create Date: 2017-03-09 17:33:24.321000

"""

# revision identifiers, used by Alembic.
revision = 'a7eae8eb920f'
down_revision = '00e723b88564'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('correlation_group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('r_squared', sa.Float(), nullable=True),
    sa.Column('asset_value', sa.Float(), nullable=True),
    sa.Column('asset_volatility', sa.Float(), nullable=True),
    sa.Column('current_liabilities', sa.Float(), nullable=True),
    sa.Column('long_term_debt', sa.Float(), nullable=True),
    sa.Column('total_debt', sa.Float(), nullable=True),
    sa.Column('market_cap', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('portfolio_result',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('portfolio_id', sa.Integer(), nullable=False),
    sa.Column('expected_return', sa.Float(), nullable=True),
    sa.Column('expected_loss', sa.Float(), nullable=True),
    sa.Column('volatility', sa.Float(), nullable=True),
    sa.Column('var_3_pct', sa.Float(), nullable=True),
    sa.Column('etl_3_pct', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio', sa.Float(), nullable=True),
    sa.Column('vasicek_ratio_3_pct', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolio.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exposure_result',
    sa.Column('exposure_id', sa.Integer(), nullable=False),
    sa.Column('expected_return', sa.Float(), nullable=True),
    sa.Column('mc_expected_loss_gross', sa.Float(), nullable=True),
    sa.Column('volatility', sa.Float(), nullable=True),
    sa.Column('risk_contribution', sa.Float(), nullable=True),
    sa.Column('tail_risk_contribution', sa.Float(), nullable=True),
    sa.Column('sharpe_ratio', sa.Float(), nullable=True),
    sa.Column('vasicek_ratio', sa.Float(), nullable=True),
    sa.Column('rorac', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['exposure_id'], ['exposure.id'], ),
    sa.PrimaryKeyConstraint('exposure_id')
    )
    op.add_column(u'company', sa.Column('correlation_group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'company', 'correlation_group', ['correlation_group_id'], ['id'])
    op.drop_column(u'company', 'create_date')
    # ### end Alembic commands ###

    op.execute("ALTER TABLE company_geography_financial_series_quarterly ALTER revenue type float")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'company', sa.Column('create_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint('company_correlation_group_id_fkey', 'company', type_='foreignkey')
    op.drop_column(u'company', 'correlation_group_id')
    op.drop_table('exposure_result')
    op.drop_table('portfolio_result')
    op.drop_table('correlation_group')
    # ### end Alembic commands ###

    op.execute("ALTER TABLE company_geography_financial_series_quarterly ALTER revenue type integer")
