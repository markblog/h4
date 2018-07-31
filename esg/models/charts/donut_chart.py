from esg.models.charts.base_charts import BaseChart
from flask import jsonify

class DonutChart(BaseChart):

	def __init__(self):
		self.type = 'donut'
		self.title = 'Donut chart'
		self.data =[{
			"name": "PortfolioA",
        	"data": [0.05, 0.09, 0.10, 0.15, 0.11, 0.38, 0.52]
		}]
		self.message = 'Here will be hint, if we get error'
		self.available_chart_type = {'donut':'donut'}

	def fetch_data(self, **kwargs):
		raise "Not Implemented"

