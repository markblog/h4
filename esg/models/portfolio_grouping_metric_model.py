from ext import db
import datetime


class PortfolioGroupingMetricModel(db.Model):
    __tablename__ = 'portfolio_grouping_metric'
    
    portfolio_metric_date_id = db.Column(db.Integer, db.ForeignKey('portfolio_metric_date.id'), primary_key=True)
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'), primary_key=True)
    grouping_id = db.Column(db.Integer, db.ForeignKey('grouping.id'), primary_key=True)
    value = db.Column(db.Float)
    
    portfolio_metric_date = db.relationship('PortfolioMetricDateModel', foreign_keys=[portfolio_metric_date_id])
    
    @property
    def serialize(self):
        return {
            'portfolio_metric_date_id': str(self.portfolio_metric_date_id),
            'metric_id': str(self.metric_id),
            'grouping_id': str(self.grouping_id),
            'value': str(self.value),
        }
