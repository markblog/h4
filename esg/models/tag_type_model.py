from ext import db
import datetime


class TagTypeModel(db.Model):
    __tablename__ = 'tag_type'
    __table_args__ = {'schema': 'meta'}
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30), nullable=False)
    tag_category_id = db.Column(db.Integer, db.ForeignKey('meta.tag_category.id'), nullable=False)
    is_from_table_data = db.Column(db.Boolean, nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'tag_category_id': str(self.tag_category_id),
            'is_from_table_data': str(self.is_from_table_data),
        }
