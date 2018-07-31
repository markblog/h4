from ext import db
import datetime


class FixedTagModel(db.Model):
    __tablename__ = 'fixed_tag'
    __table_args__ = {'schema': 'meta'}
    
    id = db.Column(db.Integer, primary_key=True)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('meta.tag_type.id'), nullable=False)
    description = db.Column(db.String(30), nullable=False)
    field_name = db.Column(db.String(30), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'tag_type_id': str(self.tag_type_id),
            'description': self.description,
            'field_name': self.field_name,
        }
