from ext import db
import datetime


class SectorModel(db.Model):
    __tablename__ = 'sector'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    
    parent = db.relationship('SectorModel', remote_side=[id])
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'level': str(self.level),
            'parent_id': str(self.parent_id),
        }
