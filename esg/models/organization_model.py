from ext import db
import datetime


class OrganizationModel(db.Model):
    __tablename__ = 'organization'
    __table_args__ = {'schema': 'membership'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    is_master = db.Column(db.Boolean, nullable=False)
    
    db.UniqueConstraint('name')
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'is_master': str(self.is_master),
        }
