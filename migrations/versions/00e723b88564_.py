"""empty message

Revision ID: 00e723b88564
Revises: b634c8e30bd7
Create Date: 2017-03-07 14:43:22.205000

"""

# revision identifiers, used by Alembic.
revision = '00e723b88564'
down_revision = 'b634c8e30bd7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("DROP SEQUENCE sector_id_seq CASCADE")
    op.execute("DROP SEQUENCE geography_id_seq CASCADE")
    op.execute("DROP SEQUENCE esg_factor_id_seq CASCADE")
    op.execute("DROP SEQUENCE asset_type_id_seq CASCADE")


def downgrade():
    op.execute("CREATE SEQUENCE sector_id_seq")
    op.execute("ALTER TABLE sector ALTER id SET DEFAULT nextval('sector_id_seq'::regclass)")
    op.execute("CREATE SEQUENCE geography_id_seq")
    op.execute("ALTER TABLE geography ALTER id SET DEFAULT nextval('geography_id_seq'::regclass)")
    op.execute("CREATE SEQUENCE esg_factor_id_seq")
    op.execute("ALTER TABLE esg_factor ALTER id SET DEFAULT nextval('esg_factor_id_seq'::regclass)")
    op.execute("CREATE SEQUENCE asset_type_id_seq")
    op.execute("ALTER TABLE asset_type ALTER id SET DEFAULT nextval('asset_type_id_seq'::regclass)")
