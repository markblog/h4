from esg.models.charts.base_charts import BaseChart
from flask import jsonify


class MapChart(BaseChart):

	def __init__(self):
		self.type = 'map'
		self.title = 'Map Chart'
		self.data =[{
			"name": "PortfolioA",
        	"data": [0.05, 0.09, 0.10, 0.15, 0.11, 0.38, 0.52]
		}]
		self.available_chart_type = {'map':'map'}

	def fetch_data(self, **kwargs):
		raise "Not Implemented"