from ext import db
import datetime


class TagHistoryModel(db.Model):
    __tablename__ = 'tag_history'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tag_combination = db.Column(db.JSON, nullable=False)
    create_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'tag_combination': self.tag_combination,
            'create_date': str(self.create_date),
            'owner_id': str(self.owner_id),
        }
