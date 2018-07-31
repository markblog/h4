from ext import db
from sqlalchemy.orm import relationship
import datetime

class ESGSimpleDemoModel(db.Model):
	__tablename__ = 'esg_simple_demo_model'

	id = db.Column(db.Integer,primary_key=True,autoincrement = True)
	company_name = db.Column(db.String(64), nullable = False)
	setup_date = db.Column(db.DateTime,default=datetime.datetime.utcnow())
	

	# def __init__(self,casename,serial_number,pass_or_not,test_date,
	# 				error_type,error_message,status,time_consume,test_set_id):
	# 	self.casename = casename
	# 	self.serial_number = serial_number
	# 	self.pass_or_not = pass_or_not
	# 	self.test_date = test_date
	# 	self.error_type = error_type
	# 	self.error_message = error_message
	# 	self.status = status
	# 	self.time_consume = time_consume
	# 	self.test_set_id = test_set_id


	def serialize(self):
		return {
			'id' : str(self.id),
			'company_name' : self.company_name,
			'setup_date' : self.setup_date,
		}
