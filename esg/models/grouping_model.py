from ext import db


class GroupingModel(db.Model):
    __tablename__ = 'grouping'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    geography_id = db.Column(db.Integer, db.ForeignKey('geography.id'))
    esg_factor_id = db.Column(db.Integer, db.ForeignKey('esg_factor.id'))
    analysis = db.Column(db.String(32))

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'sector_id': str(self.sector_id),
            'geography_id': str(self.geography_id),
            'esg_factor_id': str(self.esg_factor_id),
            'analysis': self.analysis
        }
