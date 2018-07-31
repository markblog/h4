from ext import db
import datetime


class SessionModel(db.Model):
    __tablename__ = 'session'
    __table_args__ = {'schema': 'membership'}
    
    id = db.Column(db.String(32), primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('membership.login.id'), nullable=False)
    last_activity_date = db.Column(db.DateTime, nullable=False)
    
    login = db.relationship('LoginModel', foreign_keys=[login_id])
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'login_id': str(self.login_id),
            'last_activity_date': str(self.last_activity_date),
        }
