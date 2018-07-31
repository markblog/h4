from esg.models.charts.bar_chart import BarChart
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.grouping_model import GroupingModel
from esg.models.sector_model import SectorModel
from esg.models.geography_model import GeographyModel
from esg.models.security_model import SecurityModel
from esg.models.security_contribution_model import SecurityContributionModel
from esg.models.metric_model import MetricModel
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.securities import security_services
from esg.models.exceptions.custom_exceptions import NoDataException
from ext import db

class ContributionOfSecurity(BarChart):
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
		required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.ESG_METRICS, TagTypeChart.DATE, TagTypeChart.ALL_CONTRIBUTORS]
		either_parameters = [TagTypeChart.ALL_CONTRIBUTORS,TagTypeChart.REGION,TagTypeChart.SECTOR,TagTypeChart.ALL_REGIONS_SECTORS, TagTypeChart.WEIGHT, TagTypeChart.WEIGHT_METHOD]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1),(TagTypeChart.ESG_METRICS, 1),(TagTypeChart.REGION, 1),(TagTypeChart.SECTOR, 1)]

		return[(required_parameters,either_parameters,number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])
		self._get_available_chart_type()

		portfolio = self._parameters.get(TagTypeChart.PORTFOLIO)[0]
		metric = self._parameters.get(TagTypeChart.ESG_METRICS)
		sectors = self._parameters.get(TagTypeChart.SECTOR,[])
		regions = self._parameters.get(TagTypeChart.REGION,[])
		scope_list = self._parameters.get(TagTypeChart.ALL_REGIONS_SECTORS,[])
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']

		self.subtitle = 'State Street'
		# convert the dictionary list to list dictionary
		sectors_dic = self._parse_parameters_dic_to_list(sectors)
		regions_dic = self._parse_parameters_dic_to_list(regions)

		metric_results = MetricModel.query.filter_by(id = metric[0]['id']).first()

		# self.title = 'Distribution of ' + metric_results.name + '('+metric_results.provider + ') Sector/Region'
		# process the scope_list first
		if len(scope_list) > 0 and len(scope_list) < 2:
			scope = scope_list[0]
			if scope['id'] == 2:
				if not regions_dic:
					regions_dic = {}
					regions_dic['id'] = self._get_all_regions_grouping_ids_by_level(1)
			elif scope['id'] == 3:
				if regions_dic:
					temp_ids_list = []
					for _id in regions_dic['id']:
						temp_ids_list.extend(self._get_region_all_countries_grouping_ids(_id))
					regions_dic['id'] = temp_ids_list
				else:
					regions_dic = {}
					regions_dic['id'] = self._get_all_regions_grouping_ids_by_level(2)
				
			elif scope['id'] == 4:
				if not sectors_dic:
					sectors_dic = {}
					sectors_dic['id'] = self._get_all_sectors_grouping_ids_by_level(1)
			elif scope['id'] == 5:
				if sectors_dic:
					temp_ids_list = []
					for _id in sectors_dic['id']:
						temp_ids_list.extend(self._get_sector_all_indutrials_grouping_ids(_id))
					sectors_dic['id'] = temp_ids_list
				else:
					sectors_dic = {}
					sectors_dic['id'] = self._get_all_sectors_grouping_ids_by_level(2)
				


			else:
				self.message = 'Reporting Scope can not be ESG DETAILS and UNGC DETAILS, also ALL SECURITIES'
		else:
			if len(scope_list) >= 2:
				self.message = 'Too many scope tags in this query'
			else:
				pass

		portfolio_name = portfolio['name']

		if sectors_dic and regions_dic:
			grouping_ids, categories = zip(
				*self._get_sector_region_grouping_ids(sectors_dic['id'], regions_dic['id']))
		elif sectors_dic:
			grouping_ids, categories = zip(*self._get_sector_grouping_ids(sectors_dic['id']))
		elif regions_dic:
			grouping_ids, categories = zip(*self._get_region_grouping_ids(regions_dic['id']))
		else:
			grouping_ids, categories = ['0'],[portfolio_name]

		self.xAxis['title'] = 'Security Id'
		self.title = metric_results.name + ' contribution of security in ' + categories[0]

		self.yAxis['title'] = metric_results.name + " (" + metric_results.provider + ")"

		# demonstrate the portfolio have missing data for categories, 
		# any portfolio has completed data(missing_categories = False), we will show all categories

		portfolio_data = {}
		# Todo: need to replace with latest date in security contribution
		date = security_services.get_last_available_day_until_date_in_security_contribution(date_parameters, portfolio['id'], grouping_ids[0]).strftime("%Y-%m-%d")
		grouping_id = grouping_ids[0]
		dic = {}
		dic['name'] = portfolio_name + '(' + date +')'
		print(date, portfolio['id'], grouping_id, metric[0]['id'])
		names, value = zip(*self._contribution_of_security(date, portfolio['id'], grouping_id, metric[0]['id']))
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

	def _get_sector_grouping_ids(self,sector_ids):
		"""
		get sector gouping ids according sector_ids from front-end
		"""
		grouping_results = GroupingModel.query.filter(GroupingModel.geography_id == None).\
		filter(GroupingModel.sector_id.in_(sector_ids)).\
		order_by(GroupingModel.id.asc()).all()
		ids = [(grouping.id, grouping.name) for grouping in grouping_results]
		return ids

	def _get_region_grouping_ids(self,geography_ids):
		grouping_results = GroupingModel.query.filter(GroupingModel.sector_id == None).\
		filter(GroupingModel.geography_id.in_(geography_ids)).\
		order_by(GroupingModel.id.asc()).all()
		ids = [(grouping.id, grouping.name) for grouping in grouping_results]
		return ids

	def _get_sector_region_grouping_ids(self,sector_ids, geography_ids):
		grouping_results = GroupingModel.query.filter(GroupingModel.sector_id.in_(sector_ids)).\
		filter(GroupingModel.geography_id.in_(geography_ids)).\
		order_by(GroupingModel.id.asc()).all()
		ids = [(grouping.id,grouping.name) for grouping in grouping_results]
		return ids

	def _get_sector_all_indutrials_grouping_ids(self, sector_id):
		sector_results = SectorModel.query.filter_by(parent_id=sector_id).all()
		sector_ids = [sector.id for sector in sector_results]
		return sector_ids

	def _get_region_all_countries_grouping_ids(self, geography_id):
		geography_results = GeographyModel.query.filter_by(parent_id=geography_id).all()
		geography_ids = [geography.id for geography in geography_results]
		return geography_ids

	def _get_all_sectors_grouping_ids_by_level(self,level):
		sector_results = SectorModel.query.filter_by(level = level).all()
		sector_ids = [sector.id for sector in sector_results]
		return sector_ids

	def _get_all_regions_grouping_ids_by_level(self,level):
		geography_results = GeographyModel.query.filter_by(level=level).all()
		geography_ids = [geography.id for geography in geography_results]
		return geography_ids

	def _get_exist_grouping_ids_and_names(self, grouping_ids):
		exist_grouping_results = GroupingModel.query.filter(GroupingModel.id.in_(grouping_ids)).\
		order_by(GroupingModel.id.asc()).all()

		return [(grouping.id, grouping.name) for grouping in exist_grouping_results]

	def _contribution_of_security(self,date, portfolio_id, grouping_id, metric_id):
		result = []
		security_results = SecurityContributionModel.query.filter_by(date_key = date).\
															filter_by(portfolio_id = portfolio_id).\
															filter_by(grouping_id = grouping_id).\
															filter_by(metric_id = metric_id).\
															join(SecurityModel, SecurityContributionModel.security_id==SecurityModel.id).\
															add_columns(SecurityModel.name, SecurityContributionModel.value).\
															order_by(SecurityContributionModel.value.desc()).limit(10).all()

		result = [(security.name, security.value) for security in security_results]
		if self._is_empty(result):
				raise NoDataException
		return result
