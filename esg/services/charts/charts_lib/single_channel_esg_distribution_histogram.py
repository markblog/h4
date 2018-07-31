from esg.models.charts.bar_chart import BarChart
from esg.models.exceptions.custom_exceptions import ESGException
from esg.models.grouping_model import GroupingModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric


class SingleESGDistributionHistogram(BarChart):
	"""
	This is for chart 1
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
		self._parameters = {}

	@staticmethod
	def parameter_settings():
		_required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.ESG_METRICS, TagTypeChart.BUCKETS,
								TagTypeChart.DATE]
		_either_parameters = [TagTypeChart.WEIGHT_METHOD, TagTypeChart.WEIGHT, TagTypeChart.PORTFOLIO_METRICS]
		_number_of_parameters = [(TagTypeChart.ESG_METRICS, 1), (TagTypeChart.PORTFOLIO_METRICS, 1)]

		return [(_required_parameters, _either_parameters, _number_of_parameters)]

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
		# portfolios = kwargs['portfolios']
		# esg_factors = kwargs['esg_factors']
		# metrics = kwargs['metrics']
		portfolios = self._parameters.get(TagTypeChart.PORTFOLIO)
		esg_factors = self._parameters.get(TagTypeChart.ESG_METRICS)
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']
		metrics = self._parameters.get('metrics')
		# date_parameters = kwargs['date'][0]['name']
		# process weight and weight by value
		# now it is hard code here and we also can find them by name in database, but i don't want to search by name,
		# so here is a temporary solution
		self.xAxis['title'] = 'Buckets'
		metric_id = metrics[0]['id']
		if metric_id == -3 or (metrics[0]['tag_type_id'] == 8 and metric_id == 1):
			metric_id = 14
			self.yAxis['title'] = 'Sum of the Securities Weight'
		elif metric_id == 2 and metrics[0]['tag_type_id'] == 3:
			metric_id = 12
			self.yAxis['title'] = 'Total Value of Securities'
		elif metric_id == 1 and metrics[0]['tag_type_id'] == 3:
			metric_id = 13
			self.yAxis['title'] = 'Number of Securities'
		else:
			print('No such metric')

		# Here we find the first date that data is available in portfolios
		# self.subtitle = 'Source date: ' + str(date)
		self.subtitle = 'State Street'

		grouping_ids, categories = zip(*self._get_esg_grouping_ids(esg_factors[0]['id']))

		for portfolio in portfolios:
			date = get_last_available_day_until_date_in_grouping_metric(date_parameters, portfolio,
																		grouping_ids).strftime("%Y-%m-%d")
			portfolio_grouping_metric_result = PortfolioGroupingMetricModel.query. \
				filter_by(metric_id=metric_id). \
				filter(PortfolioGroupingMetricModel.grouping_id.in_(grouping_ids)). \
				join(PortfolioGroupingMetricModel.portfolio_metric_date). \
				filter_by(portfolio_id=portfolio['id']). \
				filter_by(date_key=date). \
				order_by(PortfolioGroupingMetricModel.grouping_id.asc()).all()

			if len(portfolio_grouping_metric_result) == 0:
				raise ESGException('No data available for ')
			portfolio_data = {}
			portfolio_data['name'] = portfolio['name'] + ' (' + str(date) + ')'
			portfolio_data['data'] = [portfolio_grouping_metric.value for portfolio_grouping_metric in
									  portfolio_grouping_metric_result]
			self.data.append(portfolio_data)
		if len(portfolios) > 1:
			self.title = esg_factors[0]['name'] + ' Distribution Histogram of Multiple Portfolios'
		else:
			self.title = esg_factors[0]['name'] + ' Distribution Histogram of ' + portfolios[0]['name']

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
		if len(self._parameters.get(TagTypeChart.PORTFOLIO)) == 1 and len(self._parameters.get(TagTypeChart.ESG_METRICS)) == 1:
			self.available_chart_type = {
							'bar': 'bar',
							'radar':'radar',
							'pie':'pie'
						}
		else:
			self.available_chart_type = {
							'bar': 'bar',
							'stackedBar':'stacked bar',
							'stackedPercentageBar':'stacked percentage bar',
							'radar':'radar'
						}
