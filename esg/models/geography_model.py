from ext import db
import datetime


class GeographyModel(db.Model):
    __tablename__ = 'geography'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('geography.id'))
    code = db.Column(db.String(10)) # follow the iso_3166_1, see https://en.wikipedia.org/wiki/ISO_3166-1
    
    parent = db.relationship('GeographyModel', remote_side=[id])
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'level': str(self.level),
            'parent_id': str(self.parent_id),
            'code': self.code
        }
