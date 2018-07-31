from ext import db
import datetime


class SecurityContributionModel(db.Model):
    __tablename__ = 'security_contribution'
    
    portfolio_id = db.Column(db.Integer, db.ForeignKey('public.portfolio.id'), primary_key=True)
    security_id = db.Column(db.String(20), db.ForeignKey('public.security.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('public.metric.id'), primary_key=True)
    grouping_id = db.Column(db.Integer, db.ForeignKey('public.grouping.id'), primary_key=True)
    esg_factor_id = db.Column(db.Integer, db.ForeignKey('public.esg_factor.id'), primary_key=True)
    value = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'portfolio_id': str(self.portfolio_id),
            'security_id': self.security_id,
            'date_key': str(self.date_key),
            'metric_id': str(self.metric_id),
            'grouping_id': str(self.grouping_id),
            'esg_factor_id': str(self.esg_factor_id),
            'value': str(self.value),
        }
