from ext import db
import datetime


class LoginModel(db.Model):
    __tablename__ = 'login'
    __table_args__ = {'schema': 'membership'}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255))
    organization_id = db.Column(db.Integer, db.ForeignKey('membership.organization.id'), nullable=False)
    
    organization = db.relationship('OrganizationModel', foreign_keys=[organization_id])
    
    db.UniqueConstraint('email', 'login_name')
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'login_name': self.login_name,
            'display_name': self.display_name,
            'password': self.password,
            'email': self.email,
            'organization_id': str(self.organization_id),
        }
