from ext import db
import datetime


class AlertTypeModel(db.Model):
    __tablename__ = 'alert_type'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    text_template = db.Column(db.String(1000), nullable=False)
    target = db.Column(db.String(1), nullable=False)
    
    search_tags = db.relationship('AlertSearchTagModel', foreign_keys='AlertSearchTagModel.alert_type_id')
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'text_template': self.text_template,
            'target': self.target,
        }
