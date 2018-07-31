from ext import db
import datetime


class PortfolioSecurityModel(db.Model):
    __tablename__ = 'portfolio_security'
    
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    security_id = db.Column(db.String(20), db.ForeignKey('security.id'), primary_key=True)
    portfolio_update_date = db.Column(db.Date, primary_key=True)
    position = db.Column(db.Float, nullable=False)
    
    portfolio = db.relationship('PortfolioModel', foreign_keys=[portfolio_id])
    security = db.relationship('SecurityModel', foreign_keys=[security_id])
    
    @property
    def serialize(self):
        return {
            'portfolio_id': str(self.portfolio_id),
            'security_id': self.security_id,
            'portfolio_update_date': str(self.portfolio_update_date),
            'position': str(self.position),
        }
