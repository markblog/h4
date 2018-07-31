from ext import db
import datetime


class EsgFactorModel(db.Model):
    __tablename__ = 'esg_factor'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data_provider_id = db.Column(db.String(2), db.ForeignKey('data_provider.id'))
    level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('esg_factor.id'))
    esg_type = db.Column(db.String(1))
    weight = db.Column(db.Float)
    
    data_provider = db.relationship('DataProviderModel', foreign_keys=[data_provider_id])
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'data_provider_id': self.data_provider_id,
            'level': str(self.level),
            'parent_id': str(self.parent_id),
            'esg_type': self.esg_type,
            'weight': str(self.weight),
        }
