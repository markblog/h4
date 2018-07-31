from esg.models.charts.base_charts import BaseChart
from flask import jsonify

class BarChart(BaseChart):

	def __init__(self):
		self.type = 'bar'
		self.xAxis = {
			"categories":[1,2,3,4,5,6,7]
		}
		self.yAxis = {"title":"Weight"}
		self.data =[{
			"name": "PortfolioA",
        	"data": [0.05, 0.09, 0.10, 0.15, 0.11, 0.38, 0.52]
		}]
		self.message = 'Here will be hint, if we get error'
		self.available_chart_type = {'bar':'bar'}

	def fetch_data(self, **kwargs):
		raise "Not Implemented"

