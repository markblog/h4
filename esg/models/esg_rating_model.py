from ext import db
import datetime


class EsgRatingModel(db.Model):
    __tablename__ = 'esg_rating'
    
    data_provider_id = db.Column(db.String(2), db.ForeignKey('data_provider.id'), primary_key=True)
    id = db.Column(db.String(5), primary_key=True)
    
    @property
    def serialize(self):
        return {
            'data_provider_id': self.data_provider_id,
            'id': self.id,
        }
