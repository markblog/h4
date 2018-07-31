from ext import db


class EsgChartsModel(db.Model):
    __tablename__ = 'esg_charts'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gxid = db.Column(db.String(30))
    portfolio_type = db.Column(db.String(100))
    country_iso = db.Column(db.String(30))
    date = db.Column(db.Date)
    ungc = db.Column(db.Float)
    human_rights = db.Column(db.Float)
    labour_rights = db.Column(db.Float)
    environment = db.Column(db.Float)
    anti_corruption = db.Column(db.Float)
    environment_score = db.Column(db.Float)
    shares = db.Column(db.Float)
    prices = db.Column(db.Float)

    ara_fspermid = db.Column(db.String(30))
    country = db.Column(db.String(30))
    company_location_code = db.Column(db.String(30))
    gics_sub_industry = db.Column(db.String(30))
    sector = db.Column(db.String(50))
    regional_adjusted_log_return = db.Column(db.Float)
    usd_marketcap = db.Column(db.Float)
    social_score = db.Column(db.Float)
    governance_score = db.Column(db.Float)
    currency = db.Column(db.String(10))
    isin = db.Column(db.String(100))
    sedol = db.Column(db.String(30))
    cusip = db.Column(db.String(30))
    description = db.Column(db.String(100))
    ric = db.Column(db.String(30))
    primaryric = db.Column(db.String(100))
    fspermid = db.Column(db.String(100))
    ticker = db.Column(db.String(30))
    exchange_iso = db.Column(db.String(30))
    company_name = db.Column(db.String(100))
    usd_marketcap = db.Column(db.Float)
    annualized_return = db.Column(db.Float)
    esg = db.Column(db.Float)
    weight = db.Column(db.Float)

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'gxid': str(self.gxid),
            'portfolio_type': str(self.portfolio_type),
            'country_iso': str(self.country_iso),
            'date': str(self.date),
            'ungc': str(self.ungc),
            'human_rights': str(self.human_rights),
            'labour_rights': str(self.labour_rights),
            'environment': str(self.environment),
            'anti_corruption': str(self.anti_corruption),
            'environment_score': str(self.environment_score),
            'shares': str(self.shares),
            'prices': str(self.prices),
            'ara_fspermid': str(self.ara_fspermid),
            'country': str(self.country),
            'company_location_code': str(self.company_location_code),
            'gics_sub_industry': str(self.gics_sub_industry),
            'sector': str(self.sector),
            'regional_adjusted_log_return': str(self.regional_adjusted_log_return),
            'usd_marketcap': str(self.usd_marketcap),
            'social_score': str(self.social_score),
            'governance_score': str(self.governance_score),
            'currency': str(self.currency),
            'isin': str(self.isin),
            'sedol': str(self.sedol),
            'cusip': str(self.cusip),
            'description': str(self.description),
            'ric': str(self.ric),
            'primaryric': str(self.primaryric),
            'fspermid': str(self.fspermid),
            'ticker': str(self.ticker),
            'exchange_iso': str(self.exchange_iso),
            'company_name': str(self.company_name),
            'usd_marketcap': str(self.usd_marketcap),
            'annualized_return': str(self.annualized_return),
            'esg': str(self.esg),
            'weight': str(self.weight)
        }
