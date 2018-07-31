from esg.models.charts.scatter_chart import ScatterChart
from esg.models.portfolio_security_value_model import PortfolioSecurityValueModel
from esg.models.company_esg_factor_model import CompanyEsgFactorModel
from esg.models.portfolio_model import PortfolioModel
from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
from esg.models.esg_factor_model import EsgFactorModel
from esg.services.charts.charting_rules import TagTypeChart
from ext import db

class SingleChannelESGScoreByWeight(ScatterChart):

	def __init__(self):
		super().__init__()
		self.title = 'Single Channel ESG Score by Weight in '
		self.subtitle = 'State Street'
		self.xAxis = {
			"title": "Weight"
		}
		self.yAxis = {
			"title": "ESG Score"
		}
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.ESG_METRICS, TagTypeChart.ALL_SECURITIES, TagTypeChart.DATE]
		either_parameters = [TagTypeChart.WEIGHT_METHOD,TagTypeChart.WEIGHT]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1),(TagTypeChart.ESG_METRICS, 1)]

		return [(required_parameters, either_parameters, number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])

		portfolio_id = self._parameters.get(TagTypeChart.PORTFOLIO)[0]['id']
		portfolio = PortfolioModel.query.filter_by(id = portfolio_id).first()
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']
		date = self._get_last_evaluate_day_until_date(date_parameters, portfolio_id).strftime("%Y-%m-%d")
		portfolio_latest_updated_date = self._get_portfolio_latest_updated_date(date_parameters, portfolio_id).strftime("%Y-%m-%d")
		esg_factor_id = self._parameters.get(TagTypeChart.ESG_METRICS)[0]['id']
		esg_factor = EsgFactorModel.query.filter_by(id = esg_factor_id).first()
		self.subtitle = 'Source date: ' + str(date)
		self.title = self.title + portfolio.name
		self.xAxis['title'] = 'Weight'
		self.yAxis['title'] = esg_factor.name + ' ('+esg_factor.data_provider.name+')'

		# get security id,weight in the portfolio
		securities_companies_sql = "SELECT weight, cef.score, s.name FROM " +\
		 "(SELECT security_id, weight FROM public.portfolio_security_value WHERE portfolio_id = "+str(portfolio_id)+\
		 " AND date_key = '"+portfolio_latest_updated_date+"') psv LEFT JOIN public.security s ON psv.security_id = s.id" \
		 " LEFT JOIN public.company_esg_factor cef on s.company_id = cef.company_id" \
		 " WHERE date_key = '"+date+"' AND cef.esg_factor_id = " + str(esg_factor_id) +\
		 " ORDER BY psv.weight ASC; "

		securities_companies_results = db.engine.execute(securities_companies_sql)
		security_weight_esg_score = [{'security_id': security.name, 'x': security.weight, 'y': security.score} for security in securities_companies_results]
		self.data = [{
			"name": portfolio.name,
			"color": "rgba(78,198,226, .7)",
			"data": security_weight_esg_score
		}]

	def _get_last_evaluate_day_until_date(self, date, portfolio_id):
		# To comment here
		all_date_list = db.session.query(PortfolioEsgScoreModel.date_key).\
									distinct().\
									filter_by(portfolio_id = portfolio_id).\
									filter(PortfolioEsgScoreModel.date_key <= date).\
									order_by(PortfolioEsgScoreModel.date_key.desc()).\
									first()
		return all_date_list[0]

	def _get_portfolio_latest_updated_date(self,date, portfolio_id):
		# Here we use the latest before the last transaction day or just use the portfolio before the input date
		descend_date_list = db.session.query(PortfolioSecurityValueModel.date_key).\
									distinct().\
									filter_by(portfolio_id = portfolio_id).\
									filter(PortfolioSecurityValueModel.date_key <= date).\
									order_by(PortfolioSecurityValueModel.date_key.desc()).\
									first()

		return descend_date_list[0]
