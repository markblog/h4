from esg.models.charts.map_chart import MapChart
from esg.models.portfolio_metric_date_model import PortfolioMetricDateModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.portfolio_model import PortfolioModel
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.geography_model import GeographyModel
from esg.models.grouping_model import GroupingModel
from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
from esg.models.portfolio_security_model import PortfolioSecurityModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.portfolios.portfolio_services import get_portfolio_latest_updated_date
from ext import db

class GlobalViewOfPortfolio(MapChart):

	def __init__(self):
		super().__init__()
		self.title = 'Global View of '
		self.subtitle = 'State Street'
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.DATE, TagTypeChart.GLOBAL_MAP, TagTypeChart.ESG_METRICS]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1)]

		return [(required_parameters, None, number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])

		portfolio_id = self._parameters.get(TagTypeChart.PORTFOLIO)[0]['id']
		portfolio = PortfolioModel.query.filter_by(id = portfolio_id).first()
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']
		esg_factor_id =  self._parameters.get(TagTypeChart.ESG_METRICS)[0]['id']
		portfolio_metric_date = PortfolioMetricDateModel.query.filter_by(portfolio_id = portfolio_id).\
																	filter(PortfolioMetricDateModel.date_key <= date_parameters).\
																	order_by(PortfolioMetricDateModel.date_key.desc()).\
																	first()

		print(portfolio_metric_date.date_key)

		portfolio_esg_score = PortfolioEsgScoreModel.query.filter_by(portfolio_id = portfolio_id).\
															filter_by(esg_factor_id = esg_factor_id).\
															filter(PortfolioEsgScoreModel.date_key <= portfolio_metric_date.date_key).\
															first()


		latest_portfolio_updated_date = get_portfolio_latest_updated_date(date_parameters, portfolio_id).strftime("%Y-%m-%d")
		esg_factor = EsgFactorModel.query.filter_by(id = esg_factor_id).first()
		self.name = esg_factor.name
		self.subtitle = 'Source date: ' + str(portfolio_metric_date.date_key)
		self.title = self.title + portfolio.name

		all_countries_id = self._get_all_geography_ids_by_level(2)
		all_countries_grouping_ids, grouping_names = zip(*self._get_region_grouping_ids(all_countries_id))
		# number_of_company_in_countries_sql = "SELECT geography_id, count(*) as counts FROM " + \
		# 										"(SELECT security_id FROM public.portfolio_security where portfolio_id = "+str(portfolio_id)+" and portfolio_update_date = '"+latest_portfolio_updated_date+"') ps " + \
		# 										"LEFT JOIN public.security s ON s.id = ps.security_id " + \
		# 										"LEFT JOIN public.company c ON s.company_id = c.id " + \
		# 										"GROUP BY geography_id ORDER BY geography_id ASC"

		# number_of_company_results = db.engine.execute(number_of_company_in_countries_sql)
		# number_of_company_dic = {result.geography_id:result.counts for result in number_of_company_results}

		# portfolio_security_results = PortfolioSecurityModel.query.filter_by(portfolio_id = portfolio_id).\
		# 															filter_by(date_key = latest_portfolio_updated_date).\
		# 															all()

		# security_weight = {result.security_id, }


		# global_view_sql = "SELECT name,code,value,geography_id,ge.name as country_name FROM  ( SELECT value,grouping_id FROM public.portfolio_grouping_metric " + \
		# 					"WHERE portfolio_metric_date_id = "+str(portfolio_metric_date.id)+" AND metric_id = "+ str(esg_factor_id) +" AND grouping_id in ("+ ','.join(map(lambda id: str(id),all_countries_grouping_ids)) +")) pgm " \
		# 					"LEFT JOIN (SELECT id,geography_id FROM public.grouping WHERE sector_id is NULL AND esg_factor_id is NULL and analysis is NULL) gr ON pgm.grouping_id = gr.id " \
		# 					"LEFT JOIN (SELECT id,name,code FROM public.geography WHERE level = 2) ge ON ge.id = gr.geography_id ORDER BY geography_id ASC"

		# portfolio_grouping_metric_results = db.engine.execute(global_view_sql)

		# global_view_sql2 = "SELECT t.weighted_score as value, (t.weighted_score - "+str(portfolio_esg_score.score)+") * t.weight as weight,t.geography_id, ge.name as country_name, ge.code FROM " + \
		# 					"(SELECT geography_id, sum(weight) as weight,sum(weight*score) as weighted_score "+\
		# 						"FROM (SELECT security_id,weight FROM public.portfolio_security_value where portfolio_id = "+str(portfolio_id)+" and date_key = '"+latest_portfolio_updated_date+"') psv " +\
		# 						"LEFT JOIN public.security s ON s.id = psv.security_id " +\
		# 						"LEFT JOIN (SELECT score, company_id from company_esg_factor where date_key = '"+portfolio_metric_date.date_key.strftime("%Y-%m-%d")+"' and esg_factor_id = "+str(esg_factor_id)+") cef ON s.company_id = cef.company_id " +\
		# 						"LEFT JOIN public.company c ON s.company_id = c.id GROUP BY c.geography_id ORDER BY c.geography_id ASC) t " +\
		# 					"LEFT JOIN (SELECT id,name,code FROM public.geography WHERE level = 2) ge ON ge.id = t.geography_id"

		global_view_sql3 = "SELECT name,code,value,geography_id,ge.name as country_name,(value - "+str(portfolio_esg_score.score)+")*t.weight as weight FROM  ( SELECT value,grouping_id FROM public.portfolio_grouping_metric " + \
							"WHERE portfolio_metric_date_id = "+str(portfolio_metric_date.id)+" AND metric_id = "+ str(esg_factor_id) +" AND grouping_id in ("+ ','.join(map(lambda id: str(id),all_countries_grouping_ids)) +")) pgm " \
							"LEFT JOIN (SELECT id,geography_id FROM public.grouping WHERE sector_id is NULL AND esg_factor_id is NULL and analysis is NULL) gr ON pgm.grouping_id = gr.id " \
							"LEFT JOIN ( SELECT value as weight,grouping_id FROM public.portfolio_grouping_metric " + \
							"WHERE portfolio_metric_date_id = "+str(portfolio_metric_date.id)+" AND metric_id = 14 AND grouping_id in ("+ ','.join(map(lambda id: str(id),all_countries_grouping_ids)) +")) t ON t.grouping_id = pgm.grouping_id " \
							"LEFT JOIN (SELECT id,name,code FROM public.geography WHERE level = 2) ge ON ge.id = gr.geography_id ORDER BY geography_id ASC"

		portfolio_grouping_metric_results = db.engine.execute(global_view_sql3)



		self.max = 0
		self.min = 0

		for metric_result in portfolio_grouping_metric_results:
			dic = {}
			dic['code']  = metric_result.code
			dic['value'] = metric_result.weight  #* number_of_company_dic.get(metric_result.geography_id, 1)# * numbers_result.counts
			dic['value'] = float("{0:.2f}".format(dic['value'])) 
			if dic['value'] > self.max:
				self.max = dic['value']
			elif dic['value'] < self.min:
				self.min = dic['value']
			dic['country_name']  = metric_result.country_name
			dic['name'] = metric_result.name
			# dic['number_of_companies'] = number_of_company_dic.get(metric_result.geography_id, 1)
			dic['esg_score'] = float("{0:.2f}".format(metric_result.value))
			self.data.append(dic)

		self.data = sorted(self.data, key = lambda k: k['value'])

		# self.max = self.max
		# self.max = 100

	def _get_region_grouping_ids(self,geography_ids):
		grouping_results = GroupingModel.query.filter(GroupingModel.sector_id == None).\
		filter(GroupingModel.geography_id.in_(geography_ids)).\
		order_by(GroupingModel.id.asc()).all()
		ids = [(grouping.id, grouping.name) for grouping in grouping_results]
		return ids

	def _get_all_geography_ids_by_level(self,level):
		geography_results = GeographyModel.query.filter_by(level=level).all()
		geography_ids = [geography.id for geography in geography_results]
		return geography_ids