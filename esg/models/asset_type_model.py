from ext import db
import datetime


class AssetTypeModel(db.Model):
    __tablename__ = 'asset_type'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('asset_type.id'))
    
    @property
    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'level': str(self.level),
            'parent_id': str(self.parent_id),
        }
