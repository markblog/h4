from ext import db
import datetime


class CompanyModel(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.String(20), primary_key=True)
    ara_id = db.Column(db.String(15))
    name = db.Column(db.String(200), nullable=False)
    geography_id = db.Column(db.Integer, db.ForeignKey('geography.id'), nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))

    suppliers = db.relationship('CompanySupplierModel', foreign_keys='CompanySupplierModel.company_id')
    geography = db.relationship('GeographyModel', foreign_keys=[geography_id])
    sector = db.relationship('SectorModel', foreign_keys=[sector_id])

    @property
    def serialize(self):
        return {
            'id': self.id,
            'ara_id': self.ara_id,
            'name': self.name,
            'geography_id': str(self.geography_id),
            'sector_id': str(self.sector_id),
        }
