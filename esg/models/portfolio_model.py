from ext import db
import datetime


class PortfolioModel(db.Model):
    __tablename__ = 'portfolio'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    import_name = db.Column(db.String(200), unique=True)
    as_of = db.Column(db.Date, nullable=False)
    is_reference = db.Column(db.Boolean, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('membership.organization.id'))
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'import_name': self.import_name,
            'as_of': str(self.as_of),
            'is_reference': str(self.is_reference),
            'owner_id': str(self.owner_id),
            'create_date': str(self.create_date),
        }
