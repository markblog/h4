from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from application import app
from esg.models.charts.bar_chart import BarChart
from esg.services.charts.single_esg_distribution import SingleChannelESGScoreDistributionHistogram
from esg.services.charts.single_esg_performance_over_time import SingleChannelESGScoreTimeSeries
from esg.services.charts.single_esg_score_by_weight import SingleChannelESGScoreByWeight
from esg.request_errors import BadRequest
from ext import db


class Charting(Resource):

	def get(self):
		chart = SingleChannelESGScoreByWeight()
		# chart.fetch_data(frequency='weekly', metric_id=19, portfolio_id = 1001, grouping_ids=[464,465,466,467])
		chart.fetch_data(portfolio_id = 1001, esg_factor_id = 1, date = '2014-11-1')
		return chart.to_json()