from ext import db
import datetime


class DataProviderModel(db.Model):
    __tablename__ = 'data_provider'
    
    id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
