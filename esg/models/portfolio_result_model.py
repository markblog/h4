from ext import db
import datetime


class PortfolioResultModel(db.Model):
    __tablename__ = 'portfolio_result'
    
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    number_securities = db.Column(db.Integer)
    market_value = db.Column(db.Float)
    return_daily = db.Column(db.Float)
    cumulative_return = db.Column(db.Float)
    volatility = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    var_3_pct = db.Column(db.Float)
    etl_3_pct = db.Column(db.Float)
    expected_loss = db.Column(db.Float)
    vasicek_ratio_3_pct = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'portfolio_id': str(self.portfolio_id),
            'date_key': str(self.date_key),
            'number_securities': str(self.number_securities),
            'market_value': str(self.market_value),
            'return_daily': str(self.return_daily),
            'cumulative_return': str(self.cumulative_return),
            'volatility': str(self.volatility),
            'sharpe_ratio': str(self.sharpe_ratio),
            'var_3_pct': str(self.var_3_pct),
            'etl_3_pct': str(self.etl_3_pct),
            'expected_loss': str(self.expected_loss),
            'vasicek_ratio_3_pct': str(self.vasicek_ratio_3_pct),
        }
