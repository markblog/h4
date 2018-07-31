from ext import db
import datetime


class CompanySupplierModel(db.Model):
    __tablename__ = 'company_supplier'
    
    company_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    supplier_id = db.Column(db.String(20), db.ForeignKey('company.id'), primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    
    company = db.relationship('CompanyModel', foreign_keys=[company_id])
    supplier = db.relationship('CompanyModel', foreign_keys=[supplier_id])
    
    @property
    def serialize(self):
        return {
            'company_id': self.company_id,
            'supplier_id': self.supplier_id,
            'create_date': str(self.create_date),
        }
