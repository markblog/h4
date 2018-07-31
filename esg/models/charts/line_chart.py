from esg.models.charts.base_charts import BaseChart
from flask import jsonify


class LineChart(BaseChart):

	def __init__(self):
		self.type = 'line'
		self.xAxis = {
			"categories":[1,2,3,4,5,6,7]
		}
		self.yAxis = {"title":"Weight"}
		self.data =[{
			"name": "PortfolioA",
        	"data": [0.05, 0.09, 0.10, 0.15, 0.11, 0.38, 0.52]
		}]
		self.available_chart_type = {'line':'line'}

	def fetch_data(self, **kwargs):
		raise "Not Implemented"