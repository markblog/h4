from ext import db
import datetime


class TagCategoryModel(db.Model):
    __tablename__ = 'tag_category'
    __table_args__ = {'schema': 'meta'}
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False, unique=True)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'description': self.description,
        }
