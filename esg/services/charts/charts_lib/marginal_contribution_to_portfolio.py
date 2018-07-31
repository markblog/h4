from esg.models.charts.bar_chart import BarChart
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.grouping_model import GroupingModel
from esg.models.sector_model import SectorModel
from esg.models.geography_model import GeographyModel
from esg.models.security_model import SecurityModel
from esg.models.security_contribution_model import SecurityContributionModel
from esg.models.metric_model import MetricModel
from esg.services.portfolios import portfolio_services
from esg.services.charts.charting_rules import TagTypeChart
from esg.models.exceptions.custom_exceptions import NoDataException

from ext import db
from sqlalchemy.sql import text

class MarginalContributionToPortfolio(BarChart):
	"""
	This is for chart 3 and 4
	"""

	def __init__(self):
		super().__init__()
		self.title = 'Distribution of ESG score sector/region'
		self.subtitle = 'State Street'
		self.xAxis = {}
		self.yAxis = {}
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.ESG_METRICS, TagTypeChart.MARGINAL_CONTRIBUTION,TagTypeChart.DATE]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1), (TagTypeChart.ESG_METRICS, 1)]

		return[(required_parameters,None,number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])
		self._get_available_chart_type()

		portfolio = self._parameters.get(TagTypeChart.PORTFOLIO)[0]
		esg_factor = self._parameters.get(TagTypeChart.ESG_METRICS)[0]
		metric = self._parameters.get(TagTypeChart.MARGINAL_CONTRIBUTION)[0]
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']

		self.subtitle = 'State Street'
		portfolio_name = portfolio['name']

		self.xAxis['title'] = 'Security'
		self.title = 'Marginal contribution to ' + portfolio_name

		self.yAxis['title'] = 'Marginal contribution'

		portfolio_data = {}

		date = portfolio_services.get_portfolio_latest_updated_date(date_parameters, portfolio['id']).strftime("%Y-%m-%d")
		dic = {}
		dic['name'] = portfolio_name + '(' + date +')'

		asc_sql = """
			SELECT name, contribution FROM (SELECT q.security_id, (score-x.mean_esg_metric)*(q.BASE_CURRENCY_VALUE/x.sum_base) contribution FROM
			(SELECT SUM(base_currency_value*score)/SUM(base_currency_value) mean_esg_metric, SUM(base_currency_value) sum_base 
			FROM portfolio_security_value p
			JOIN portfolio_esg_score e ON p.portfolio_id = e.portfolio_id AND p.date_key = e.date_key AND e.esg_factor_id = :esg_factor_id
			WHERE p.portfolio_id = :portfolio_id AND p.date_key = :date_key) x
			JOIN portfolio_security_value q ON 1=1
			JOIN portfolio_esg_score f ON q.portfolio_id = f.portfolio_id AND q.date_key = f.date_key AND f.esg_factor_id = :esg_factor_id
			WHERE q.portfolio_id = :portfolio_id AND q.date_key = :date_key
			ORDER BY 2 ASC
			LIMIT 20) t
			LEFT JOIN public.security s ON t.security_id = s.id
			ORDER BY contribution DESC
		"""

		desc_sql = """
			SELECT name, contribution FROM (SELECT q.security_id, (score-x.mean_esg_metric)*(q.BASE_CURRENCY_VALUE/x.sum_base) contribution FROM
			(SELECT SUM(base_currency_value*score)/SUM(base_currency_value) mean_esg_metric, SUM(base_currency_value) sum_base 
			FROM portfolio_security_value p
			JOIN portfolio_esg_score e ON p.portfolio_id = e.portfolio_id AND p.date_key = e.date_key AND e.esg_factor_id = :esg_factor_id
			WHERE p.portfolio_id = :portfolio_id AND p.date_key = :date_key) x
			JOIN portfolio_security_value q ON 1=1
			JOIN portfolio_esg_score f ON q.portfolio_id = f.portfolio_id AND q.date_key = f.date_key AND f.esg_factor_id = :esg_factor_id
			WHERE q.portfolio_id = :portfolio_id AND q.date_key = :date_key
			ORDER BY 2 DESC
			LIMIT 20) t
			LEFT JOIN public.security s ON t.security_id = s.id
			ORDER BY contribution DESC
		"""
		sql = desc_sql if metric['id'] == 100 else asc_sql
		parameters = {'portfolio_id':portfolio['id'], 'esg_factor_id':esg_factor['id'], 'date_key':date}
		results_proxy = db.engine.execute(text(sql),parameters)
		results = [(security.name, security.contribution) for security in results_proxy]
		names, value = zip(*results)
		dic['data'] = value
		self.xAxis['categories'] = names
		self.data.append(dic)

	def _get_available_chart_type(self):
		if len(self._parameters.get(TagTypeChart.PORTFOLIO)) > 1:
			self.available_chart_type = {
							'bar': 'bar',
							'stackedBar':'stacked bar',
							'stackedPercentageBar':'stacked percentage bar',
							'radar':'radar'
						}
		else:
			self.available_chart_type = {
							'bar': 'bar',
							'radar':'radar',
							'pie':'pie'
						}