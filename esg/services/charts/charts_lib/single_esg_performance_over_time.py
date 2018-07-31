from esg.models.charts.line_chart import LineChart
from esg.models.metric_model import MetricModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.charts.portfolio_time_frequency import PortfolioTimeFrequency

from ext import db
from esg.models.grouping_model import GroupingModel


class SingleChannelESGPerformanceTimeSeries(LineChart):
	def __init__(self):
		super().__init__()
		self.title = 'Performance by single-channel ESG score time series'
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
		self.yAxis = {"title": "portfolio value"}
		self.data = []
		self._value_dic = {'Cumulative Return': 'Cumulative Return',
						  'Return (daily)': 'Return Daily',
						  'Market Value': 'Market Value',
						  'Number of securities': 'Number of Securities',
						  'Weight by value': 'Weight',
						  }
		self._grouping_dic = {'Arabesque UNGC': [473, 474, 475, 476],
							 'Arabesque UNGC Human Rights': [477, 478, 479, 480],
							 'Arabesque UNGC Labour Rights': [481, 482, 483, 484],
							 'Arabesque UNGC Environment': [485, 486, 487, 488],
							 'Arabesque UNGC Anti Corruption': [489, 490, 491, 492],
							 'Arabesque ESG': [493, 494, 495, 496],
							 'Arabesque ESG Environment Score': [497, 498, 499, 500],
							 'Arabesque ESG Social Score': [501, 502, 503, 504],
							 'Arabesque ESG Governance Score': [505, 506, 507, 508]
							 }

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.ESG_METRICS, TagTypeChart.TIME, TagTypeChart.PORTFOLIO_METRICS, TagTypeChart.ANALYSIS]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1), (TagTypeChart.ESG_METRICS, 1),(TagTypeChart.PORTFOLIO_METRICS, 1)]

		return [(required_parameters,None,number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])
		esg_factor_list_para = []
		line_data = {}
		portfolios_value = self._parameters.get(TagTypeChart.PORTFOLIO)
		market_list = self._parameters.get(TagTypeChart.PORTFOLIO_METRICS)
		esg_factor_list = self._parameters.get(TagTypeChart.ESG_METRICS)
		frequency = self._parameters.get(TagTypeChart.TIME)[0]['id']
		time_frequency = PortfolioTimeFrequency()

		grouping_results = GroupingModel.query.filter(GroupingModel.esg_factor_id == esg_factor_list[0]['id'],GroupingModel.analysis == 'top').all()
		grouping_id = [grouping.id for grouping in grouping_results]
		grouping_ids = [grouping_id[0], grouping_id[0]+1,grouping_id[0]+2,grouping_id[0]+3]
		
		for market in market_list:
			esg_factor_para = market['name']
			market_list_para = [value for key, value in self._value_dic.items() if key == esg_factor_para]
			metric_num = MetricModel.query.filter(MetricModel.name == market_list_para[0]).all()
			metric_id = [model.id for model in metric_num]
			
		for esg_factor in esg_factor_list:
			esg_factor_para = esg_factor['name']
			esg_factor_list_para.append(esg_factor_para)
			# frequency = time_list[0]['name']
			# frequency = [value for key, value in self.time_dic.items() if key == frequency]

		value_str = 'market_value'
		self.xAxis['title'] = 'Time series'
		self.yAxis['title'] = 'Market Value'
		if metric_id[0] == 10:
			value_str = 'cumulative_return'
			self.yAxis['title'] = 'Cumulative Return'
		elif metric_id[0] == 11:
			value_str = 'return_daily'
			self.yAxis['title'] = 'Return Daily'
		elif metric_id[0] == 13:
			value_str = 'number_securities'
			self.yAxis['title'] = 'Number of Securities'

		portfolio_id, portfolio_name = zip(*self._get_portfolio_id_and_name(portfolios_value))

		if frequency == 4:
			date_list = time_frequency._is_last_transaction_day_of_a_week(portfolio_id[0])
		elif frequency == 3:
			date_list = time_frequency._is_last_transaction_day_of_a_month(portfolio_id[0])
		elif frequency == 2:
			date_list = time_frequency._is_last_transaction_day_of_a_quarter(portfolio_id[0])
		elif frequency == 1:
			date_list = time_frequency._is_last_transaction_day_of_a_year(portfolio_id[0])
		else:
			date_list = time_frequency._all_date(portfolio_id[0])
			date_list = [date.date_key.strftime('%Y-%m-%d') for date in date_list]
		date_list.reverse()
		self.xAxis['categories'] = date_list
		date_sql_list = ','.join(map(self.quote_element, date_list))

		portfolio_result_sql = "SELECT date_key, " + value_str + " as value FROM public.portfolio_result WHERE " \
																 "portfolio_id = " + str(portfolio_id[0]) + \
							   " AND date_key IN ( " + date_sql_list + " ) ORDER BY date_key ASC"

		portfolio_result = db.engine.execute(portfolio_result_sql)
		portfolio_result_data = [value.value for value in portfolio_result]
		line_data['name'] = 'Full portfolio'
		line_data['data'] = portfolio_result_data
		self.data.append(line_data)

		name = ['Top 1/3 of ' + portfolio_name[0],
				'Middle 1/3 of ' + portfolio_name[0],
				'Bottom 1/3 of ' + portfolio_name[0],
				'Long top 1/3 of ' + portfolio_name[0] +
				' and short bottom 1/3 of ' + portfolio_name[0]]
		grouping_ids_names = zip(grouping_ids, name)

		for id, name in grouping_ids_names:
			portfolio_result_sql = "SELECT date_key, value FROM public.portfolio_grouping_metric pgm " + \
				"JOIN public.portfolio_metric_date pd on pgm.portfolio_metric_date_id = pd.id WHERE portfolio_id = " + str(
				portfolio_id[0]) + " AND metric_id = " + str(
				metric_id[0]) + " AND grouping_id = " + str(id) + " AND date_key IN( " \
								   + date_sql_list + " ) ORDER BY date_key "
			grouping_metrics_result = db.engine.execute(portfolio_result_sql)
			grouping_metrics_data = [value.value for value in grouping_metrics_result]
			line_data = {'name': name}
			line_data['data'] = grouping_metrics_data
			self.data.append(line_data)
		self.title = portfolio_name[0] + "'s Performance by " + esg_factor_list[0]['name'] + ' Time Series'

	def _get_portfolio_id_and_name(self, portfolio_value):
		ids = [(portfolio['id'], portfolio['name']) for portfolio in portfolio_value]
		return ids

	def quote_element(self, item):
		return "'" + str(item) + "'"
