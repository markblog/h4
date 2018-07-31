from ext import db
import datetime


class SecurityModel(db.Model):
    __tablename__ = 'security'
    
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), nullable=False)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'), nullable=False)
    isin = db.Column(db.String(12))
    sedol = db.Column(db.String(7))
    cusip = db.Column(db.String(9))
    
    company = db.relationship('CompanyModel', foreign_keys=[company_id])
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'company_id': self.company_id,
            'asset_type_id': str(self.asset_type_id),
            'isin': self.isin,
            'sedol': self.sedol,
            'cusip': self.cusip,
        }
