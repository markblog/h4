from ext import db


class WeightMethodModel(db.Model):
    __tablename__ = 'weight_method'
    __table_args__ = {'schema': 'public'}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name
        }
