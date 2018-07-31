from ext import db
import datetime


class CompanyPrimarySecurityModel(db.Model):
    __tablename__ = 'company_primary_security'
    
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    asset_type_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'), primary_key=True)
    security_id = db.Column(db.String(20), db.ForeignKey('security.id'))
    
    company = db.relationship('CompanyModel', foreign_keys=[company_id])
    security = db.relationship('SecurityModel', foreign_keys=[security_id])
    
    @property
    def serialize(self):
        return {
            'company_id': self.company_id,
            'asset_type_id': str(self.asset_type_id),
            'security_id': self.security_id,
        }
