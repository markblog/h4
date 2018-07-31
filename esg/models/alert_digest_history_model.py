from ext import db
import datetime


class AlertDigestHistoryModel(db.Model):
    __tablename__ = 'alert_digest_history'
    
    alert_history_id = db.Column(db.Integer, db.ForeignKey('public.alert_history.id'), primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('membership.login.id'), primary_key=True)
    is_dismissed = db.Column(db.Boolean, nullable=False)
    
    @property
    def serialize(self):
        return {
            'alert_history_id': str(self.alert_history_id),
            'login_id': str(self.login_id),
            'is_dismissed': str(self.is_dismissed),
        }
