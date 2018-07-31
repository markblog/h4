from ext import db
import datetime


class PortfolioEsgScoreModel(db.Model):
    __tablename__ = 'portfolio_esg_score'
    
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    esg_factor_id = db.Column(db.Integer, db.ForeignKey('esg_factor.id'), primary_key=True)
    weight_method = db.Column(db.Integer)
    score = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'portfolio_id': str(self.portfolio_id),
            'date_key': str(self.date_key),
            'esg_factor_id': str(self.esg_factor_id),
            'weight_method': str(self.weight_method),
            'score': str(self.score),
        }
