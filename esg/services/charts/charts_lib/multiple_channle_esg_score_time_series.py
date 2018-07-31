from esg.models.charts.line_chart import LineChart
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.charts.portfolio_time_frequency import PortfolioTimeFrequency


class MultipleChannelEsgScoreTimSeries(LineChart):
	"""
	   This is for chart six
	   """

	def __init__(self):
		super().__init__()
		self.title = ' '
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
				"90 - 100"
			]
		}
		self.yAxis = {'title': ''}
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.TIME, TagTypeChart.WEIGHT_METHOD]
		either_parameters = [TagTypeChart.ESG_METRICS,TagTypeChart.DETAILS]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1)]

		return [(required_parameters, either_parameters, number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):
		self._parse_parameters(kwargs['parameters_dic'])

		portfolios_value = self._parameters.get(TagTypeChart.PORTFOLIO)
		frequency = self._parameters.get(TagTypeChart.TIME)[0]['id']
		weight_method_value = self._parameters.get(TagTypeChart.WEIGHT_METHOD)
		esg_factors_value = self._parameters.get(TagTypeChart.ESG_METRICS,[])
		esg_details = self._parameters.get(TagTypeChart.DETAILS,[])

		if esg_details and len(esg_details) == 1:
			if esg_details[0]['id'] == 20:
				esg_factor_results = EsgFactorModel.query.filter_by(data_provider_id='AE')
				esg_factors_value = [{"id": factor.id, "name": factor.name, "provider_name": "Arabesque_ESG"} for factor in
									 esg_factor_results]
			else:
				esg_factor_results = EsgFactorModel.query.filter_by(data_provider_id='AU')
				esg_factors_value = [{"id": factor.id, "name": factor.name,  "provider_name": "Arabesque_UNGC"} for factor in esg_factor_results]
		zipped_list = []
		union_set = set()
		
		for esg_factor in esg_factors_value:
			date_list = self.get_datelist_for_esg(frequency, portfolios_value[0]['id'])
			scores = PortfolioEsgScoreModel.query \
				.filter_by(portfolio_id=portfolios_value[0]['id']) \
				.filter_by(weight_method=weight_method_value[0]['id']) \
				.filter(PortfolioEsgScoreModel.esg_factor_id == esg_factor['id'],
						PortfolioEsgScoreModel.date_key.in_(date_list)) \
				.order_by(PortfolioEsgScoreModel.date_key.asc()).all()
			esg_dic = {esg.date_key.strftime("%Y-%m-%d"): esg.score for esg in scores}
			zipped_list.append(esg_dic)
			union_set = union_set.union(esg_dic.keys())

		for index, esg in enumerate(esg_factors_value):
			esg_factor_data = {}
			temp_dic = zipped_list[index]
			union_list = list(union_set)
			union_list.sort()
			data_list = []
			for date in union_list:
				if date not in temp_dic.keys():
					data_list.append(None)
				else:
					data_list.append(temp_dic.get(date))
			esg_factor_data['name'] = esg_factors_value[index]['name']
			esg_factor_data['data'] = data_list
			self.data.append(esg_factor_data)
		self.yAxis['title'] = 'Value-weighted Score ' + ' ('+ esg_factor['provider_name']+')'
		self.xAxis['title'] = 'Time series'
		self.xAxis['categories'] = union_list
		self.title = 'Multiple Channel ESG Score Time Series of ' + portfolios_value[0]['name']

	def get_datelist_for_esg(self, frequency, portfolio_id):
		time_frequency = PortfolioTimeFrequency()

		if frequency == 4: # weekly
			date_list = time_frequency._is_last_transaction_day_of_a_week(portfolio_id)
		elif frequency == 3: # monthly
			date_list = time_frequency._is_last_transaction_day_of_a_month(portfolio_id)
		elif frequency == 2: # quarterly
			date_list = time_frequency._is_last_transaction_day_of_a_quarter(portfolio_id)
		elif frequency == 1: # yearly
			date_list = time_frequency._is_last_transaction_day_of_a_year(portfolio_id)
		else:
			date_list = time_frequency._all_date(portfolio_id)
			date_list = [date.date_key.strftime('%Y-%m-%d') for date in date_list]
		date_list.reverse()
		return date_list

	def _get_esg_id_and_name(self, esg_factors_value):
		ids = [(esg_factor['id'], esg_factor['name']) for esg_factor in esg_factors_value]
		return ids
