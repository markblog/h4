from ext import db
import datetime


class PortfolioSecurityValueModel(db.Model):
    __tablename__ = 'portfolio_security_value'
    
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    security_id = db.Column(db.String(20), db.ForeignKey('security.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    weight = db.Column(db.Float)
    base_currency_value = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'portfolio_id': str(self.portfolio_id),
            'security_id': self.security_id,
            'date_key': str(self.date_key),
            'weight': str(self.weight),
            'base_currency_value': str(self.base_currency_value),
        }
