from ext import db
import datetime


class SecurityFinancialSeriesModel(db.Model):
    __tablename__ = 'security_financial_series'
    
    security_id = db.Column(db.String(20), db.ForeignKey('security.id'), primary_key=True)
    date_key = db.Column(db.Date, primary_key=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    closing_price = db.Column(db.Float)
    volume = db.Column(db.Float)
    return_daily = db.Column(db.Float)
    return_daily_log = db.Column(db.Float)
    return_daily_cumulative = db.Column(db.Float)
    return_daily_log_cumulative = db.Column(db.Float)
    volatility = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    vasicek_ratio = db.Column(db.Float)
    mc_expected_loss_gross = db.Column(db.Float)
    risk_contribution = db.Column(db.Float)
    tail_risk_contribution  = db.Column(db.Float)
    rorac = db.Column(db.Float)
    
    security = db.relationship('SecurityModel', foreign_keys=[security_id])
    
    @property
    def serialize(self):
        return {
            'security_id': self.security_id,
            'date_key': str(self.date_key),
            'sector_id': str(self.sector_id),
            'closing_price': str(self.closing_price),
            'volume': str(self.volume),
            'return_daily': str(self.return_daily),
            'return_daily_log': str(self.return_daily_log),
            'return_daily_cumulative': str(self.return_daily_cumulative),
            'return_daily_log_cumulative': str(self.return_daily_log_cumulative),
            'volatility': str(self.volatility),
            'sharpe_ratio': str(self.sharpe_ratio),
            'vasicek_ratio': str(self.vasicek_ratio),
            'mc_expected_loss_gross': str(self.mc_expected_loss_gross),
            'risk_contribution': str(self.risk_contribution),
            'tail_risk_contribution ': str(self.tail_risk_contribution ),
            'rorac': str(self.rorac),
        }
