from ext import db
import datetime


class CompanyEsgSummaryModel(db.Model):
    __tablename__ = 'company_esg_summary'
    
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    data_provider_id = db.Column(db.String(2), db.ForeignKey('data_provider.id'), primary_key=True)
    rating_id = db.Column(db.String(5))
    esg_score = db.Column(db.Float)
    e_score = db.Column(db.Float)
    s_score = db.Column(db.Float)
    g_score = db.Column(db.Float)
    revenue = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'company_id': self.company_id,
            'data_provider_id': self.data_provider_id,
            'rating_id': self.rating_id,
            'esg_score': str(self.esg_score),
            'e_score': str(self.e_score),
            's_score': str(self.s_score),
            'g_score': str(self.g_score),
            'revenue': str(self.revenue),
        }
