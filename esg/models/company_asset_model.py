from ext import db
import datetime


class CompanyAssetModel(db.Model):
    __tablename__ = 'company_asset'
    
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'), primary_key=True)
    volume = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'company_id': self.company_id,
            'asset_type_id': str(self.asset_type_id),
            'volume': str(self.volume),
        }
