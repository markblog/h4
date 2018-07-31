from ext import db
import datetime


class PortfolioMetricDateModel(db.Model):
    __tablename__ = 'portfolio_metric_date'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    date_key = db.Column(db.Date, nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'portfolio_id': str(self.portfolio_id),
            'date_key': str(self.date_key),
        }
