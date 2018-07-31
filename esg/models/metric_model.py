from ext import db


class MetricModel(db.Model):
    __tablename__ = 'metric'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(20), nullable=False)

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'provider': self.provider
        }
