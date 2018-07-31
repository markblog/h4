from sqlalchemy import or_

from esg.models.charts.bar_chart import BarChart
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.grouping_model import GroupingModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric
from esg.models.exceptions.custom_exceptions import NoDataException

class MultipleESGDistributionHistogram(BarChart):
	"""
	This is for chart 2
	"""

	def __init__(self):
		super().__init__()
		self.title = 'Distribution of ESG score sector/region'
		self.subtitle = 'State Street'
		self.xAxis = {
			"categories": [
				"0 - 10",
				"10 - 20",
				"20 - 30",
				"30 - 40",
				"40 - 50",
				"50 - 60",
				"60 - 70",
				"70 - 80",
				"80 - 90",
				"90 - 100",
				"unclassified"
			]
		}
		self.yAxis = {}
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters_A = [TagTypeChart.PORTFOLIO, TagTypeChart.ESG_METRICS, TagTypeChart.BUCKETS,
								 TagTypeChart.DATE]
		either_parameters_A = [TagTypeChart.WEIGHT,TagTypeChart.WEIGHT_METHOD, TagTypeChart.PORTFOLIO_METRICS]
		number_of_parameters_A = [(TagTypeChart.PORTFOLIO, 1), (TagTypeChart.PORTFOLIO_METRICS, 1)]

		required_parameters_B = [TagTypeChart.PORTFOLIO, TagTypeChart.DETAILS, TagTypeChart.BUCKETS, TagTypeChart.DATE]
		either_parameters_B = [TagTypeChart.WEIGHT, TagTypeChart.WEIGHT_METHOD,TagTypeChart.PORTFOLIO_METRICS]
		number_of_parameters_B = [(TagTypeChart.PORTFOLIO, 1), (TagTypeChart.DETAILS, 1),
								  (TagTypeChart.PORTFOLIO_METRICS, 1)]

		return [(required_parameters_A, either_parameters_A, number_of_parameters_A),
				(required_parameters_B, either_parameters_B, number_of_parameters_B)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic
		metrics = []
		metrics.extend(self._parameters.get(TagTypeChart.PORTFOLIO_METRICS, []))
		metrics.extend(self._parameters.get(TagTypeChart.WEIGHT, []))
		metrics.extend(self._parameters.get(TagTypeChart.WEIGHT_METHOD, []))
		self._parameters['metrics'] = metrics

	def fetch_data(self, **kwargs):
		self._parse_parameters(kwargs['parameters_dic'])
		self._get_available_chart_type()

		portfolios = self._parameters.get(TagTypeChart.PORTFOLIO)
		esg_factors = self._parameters.get(TagTypeChart.ESG_METRICS)
		esg_details = self._parameters.get(TagTypeChart.DETAILS)
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']
		metrics = self._parameters.get('metrics')

		metric_id = metrics[0]['id']
		self.xAxis['title'] = 'Buckets'
		if metric_id == -3 or (metrics[0]['tag_type_id'] == 8 and metric_id == 1):
			metric_id = 14
			self.yAxis['title'] = 'Sum of the Securities Weight'
		elif metric_id == 2 and metrics[0]['tag_type_id'] == 3:
			metric_id = 12
			self.yAxis['title'] = 'Total Value of Securities'
		elif metric_id == 1 and metrics[0]['tag_type_id'] == 3:
			metric_id = 13
			self.yAxis['title'] = 'Number of Securities'
		elif metric_id == 3 and metrics[0]['tag_type_id'] == 3:
			metric_id = 10
			self.yAxis['title'] = 'Cumulative Return'
		elif metric_id == 4 and metrics[0]['tag_type_id'] == 3:
			metric_id = 11
			self.yAxis['title'] = 'Return Daily'
		else:
			print('No such metric')

		if esg_details and len(esg_details) == 1:
			if esg_details[0]['id'] == 20:
				esg_factor_results = EsgFactorModel.query.filter(
					or_(EsgFactorModel.level == 1, EsgFactorModel.level == 2)).filter_by(data_provider_id='AE')
			else:
				esg_factor_results = EsgFactorModel.query.filter(
					or_(EsgFactorModel.level == 1, EsgFactorModel.level == 2)).filter_by(data_provider_id='AU')

			esg_factors = [{"id": factor.id, "name": factor.name} for factor in esg_factor_results]

		grouping_ids, _ = zip(*self._get_esg_grouping_ids(esg_factors[0]['id']))
		date = get_last_available_day_until_date_in_grouping_metric(date_parameters, portfolios[0],
																	grouping_ids).strftime("%Y-%m-%d")
		if date:
			self.subtitle = 'Source date: ' + str(date)
			if len(metrics) > 1:
				self.message = 'Two or more metrics was selected, Only the first one will be displayed'

			for factor in esg_factors:
				grouping_ids, _ = zip(*self._get_esg_grouping_ids(factor['id']))
				portfolio_grouping_metric_result = PortfolioGroupingMetricModel.query. \
					filter_by(metric_id=metric_id). \
					filter(PortfolioGroupingMetricModel.grouping_id.in_(grouping_ids)). \
					join(PortfolioGroupingMetricModel.portfolio_metric_date). \
					filter_by(portfolio_id=portfolios[0]['id']). \
					filter_by(date_key=date). \
					order_by(PortfolioGroupingMetricModel.grouping_id.asc()).all()

				esg_data = {}
				esg_data['name'] = factor['name']
				esg_data['data'] = [portfolio_grouping_metric.value for portfolio_grouping_metric in
									portfolio_grouping_metric_result]

				if self._is_empty(esg_data['data']):
					raise NoDataException

				self.data.append(esg_data)

			self.title = 'Multiple Channel ESG Score Distribution Histogram of ' + portfolios[0]['name']
		else:
			raise 'No data available on this day.'

	def _get_esg_grouping_ids(self, esg_factor_id):
		"""
		get sector gouping ids according sector_ids from front-end
		"""
		groupinp_results = GroupingModel.query.filter_by(esg_factor_id=esg_factor_id). \
			filter_by(analysis='bucket'). \
			order_by(GroupingModel.id.asc()).all()
		ids = [(grouping.id, grouping.name) for grouping in groupinp_results]
		return ids

	def _get_available_chart_type(self):
		self.available_chart_type = {
						'bar': 'bar',
						'stackedBar':'stacked bar',
						'stackedPercentageBar':'stacked percentage bar',
						'radar':'radar'
					}
