from ext import db
import datetime


class CompanyEsgFactorModel(db.Model):
    __tablename__ = 'company_esg_factor'
    
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    esg_factor_id = db.Column(db.Integer, db.ForeignKey('esg_factor.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    score = db.Column(db.Float)
    
    esg_factor = db.relationship('EsgFactorModel', foreign_keys=[esg_factor_id])
    
    @property
    def serialize(self):
        return {
            'company_id': self.company_id,
            'esg_factor_id': str(self.esg_factor_id),
            'date_key': str(self.date_key),
            'score': str(self.score),
        }
