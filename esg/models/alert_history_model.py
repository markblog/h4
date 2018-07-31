from ext import db
import datetime


class AlertHistoryModel(db.Model):
    __tablename__ = 'alert_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_type_id = db.Column(db.Integer, db.ForeignKey('public.alert_type.id'), nullable=False)
    date_key = db.Column(db.Date, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('public.portfolio.id'))
    portfolio_name = db.Column(db.String(200))
    company_id = db.Column(db.String(20), db.ForeignKey('public.company.id'))
    company_name = db.Column(db.String(200))
    data_provider_id = db.Column(db.String(2), db.ForeignKey('public.data_provider.id'))
    data_provider_name = db.Column(db.String(20))
    esg_factor_id = db.Column(db.Integer, db.ForeignKey('public.esg_factor.id'))
    esg_factor_name = db.Column(db.String(50))
    region_id = db.Column(db.Integer, db.ForeignKey('public.geography.id'))
    region_name = db.Column(db.String(200))
    country_id = db.Column(db.Integer, db.ForeignKey('public.geography.id'))
    country_name = db.Column(db.String(200))
    sector_id = db.Column(db.Integer, db.ForeignKey('public.sector.id'))
    sector_name = db.Column(db.String(50))
    industry_id = db.Column(db.Integer, db.ForeignKey('public.sector.id'))
    industry_name = db.Column(db.String(50))
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'alert_type_id': str(self.alert_type_id),
            'date_key': str(self.date_key),
            'portfolio_id': str(self.portfolio_id),
            'portfolio_name': self.portfolio_name,
            'company_id': self.company_id,
            'company_name': self.company_name,
            'data_provider_id': self.data_provider_id,
            'data_provider_name': self.data_provider_name,
            'esg_factor_id': str(self.esg_factor_id),
            'esg_factor_name': self.esg_factor_name,
            'region_id': str(self.region_id),
            'region_name': self.region_name,
            'country_id': str(self.country_id),
            'country_name': self.country_name,
            'sector_id': str(self.sector_id),
            'sector_name': self.sector_name,
            'industry_id': str(self.industry_id),
            'industry_name': self.industry_name,
        }
