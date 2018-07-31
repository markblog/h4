from esg.models.charts.base_charts import BaseChart
from flask import jsonify

class ScatterChart(BaseChart):

	def __init__(self):
		super().__init__()
		self.type = 'scatter'
		self.xAxis = {
			"text": "xAxis text"
		}
		self.yAxis = {"text":"yAxis text"}
		self.data =[{
			"name": "PortfolioA",
        	"data": [[174.0, 65.6], [175.3, 71.8], [193.5, 80.7], [186.5, 72.6], [187.2, 78.8]]
		},
		{
			"name": "PortfolioB",
        	"data": [[161.2, 51.6], [167.5, 59.0], [159.5, 49.2], [157.0, 63.0], [155.8, 53.6]]
		}]
		self.available_chart_type = {'scatter':'scatter'}

	def fetch_data(self, **kwargs):
		raise "Not Implemented"