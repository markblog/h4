from ext import db
import datetime


class CorrelationGroupModel(db.Model):
    __tablename__ = 'correlation_group'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    r_squared = db.Column(db.Float)
    asset_value = db.Column(db.Float)
    asset_volatility = db.Column(db.Float)
    current_liabilities = db.Column(db.Float)
    long_term_debt = db.Column(db.Float)
    total_debt = db.Column(db.Float)
    market_cap = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'r_squared': str(self.r_squared),
            'asset_value': str(self.asset_value),
            'asset_volatility': str(self.asset_volatility),
            'current_liabilities': str(self.current_liabilities),
            'long_term_debt': str(self.long_term_debt),
            'total_debt': str(self.total_debt),
            'market_cap': str(self.market_cap),
        }
