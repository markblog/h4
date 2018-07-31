from ext import db
import datetime


class ExchangeRateModel(db.Model):
    __tablename__ = 'exchange_rate'
    
    currency_id = db.Column(db.String(3), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    adjusted_close_price = db.Column(db.Float)
    usd_return_daily_log = db.Column(db.Float)
    usd_return_log_cumulative_sum = db.Column(db.Float)
    
    @property
    def serialize(self):
        return {
            'currency_id': self.currency_id,
            'date_key': str(self.date_key),
            'adjusted_close_price': str(self.adjusted_close_price),
            'usd_return_daily_log': str(self.usd_return_daily_log),
            'usd_return_log_cumulative_sum': str(self.usd_return_log_cumulative_sum),
        }
