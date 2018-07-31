from ext import db
import datetime


class AlertSearchTagModel(db.Model):
    __tablename__ = 'alert_search_tag'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alert_type_id = db.Column(db.Integer, db.ForeignKey('public.alert_type.id'), nullable=False)
    tag_type_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer)
    tag_name = db.Column(db.String(50))
    level = db.Column(db.Integer)
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'alert_type_id': str(self.alert_type_id),
            'tag_type_id': str(self.tag_type_id),
            'tag_id': str(self.tag_id),
            'tag_name': self.tag_name,
            'level': str(self.level),
        }
