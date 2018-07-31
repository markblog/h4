from ext import db
import datetime


class AlertSubstitutionValueModel(db.Model):
    __tablename__ = 'alert_substitution_value'
    
    alert_history_id = db.Column(db.Integer, db.ForeignKey('public.alert_history.id'), primary_key=True)
    index = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100))
    
    @property
    def serialize(self):
        return {
            'alert_history_id': str(self.alert_history_id),
            'index': str(self.index),
            'value': self.value,
        }
