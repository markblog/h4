from esg.models.charts.bar_chart import BarChart
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.grouping_model import GroupingModel
from esg.models.sector_model import SectorModel
from esg.models.geography_model import GeographyModel
from esg.models.metric_model import MetricModel
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric
from esg.services.charts.charting_rules import TagTypeChart
from ext import db

class DistributionOfESGScoresBySectorOrRegion(BarChart):
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
		required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.ESG_METRICS, TagTypeChart.DATE, TagTypeChart.WEIGHT_METHOD]
		either_parameters = [TagTypeChart.REGION,TagTypeChart.SECTOR, TagTypeChart.ALL_REGIONS_SECTORS]
		number_of_parameters = [(TagTypeChart.ESG_METRICS, 1)]

		return[(required_parameters,either_parameters,number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])
		self._get_available_chart_type()

		portfolios = self._parameters.get(TagTypeChart.PORTFOLIO)
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

		if (len(portfolios)) > 1:
			portfolio_name = 'Multiple Portfolios'
		else:
			portfolio_name = portfolios[0]['name']

		if sectors_dic and regions_dic:
			grouping_ids, categories = zip(
				*self._get_sector_region_grouping_ids(sectors_dic['id'], regions_dic['id']))
			self.xAxis['title'] = 'Region cross sector'
			self.title = metric_results.name + ' Distribution of ' + portfolio_name + ' Flitered by Region and Sector'
		elif sectors_dic:
			grouping_ids, categories = zip(*self._get_sector_grouping_ids(sectors_dic['id']))
			self.xAxis['title'] = 'Sector'
			self.title = 'Distribution of ' + portfolio_name + ' ' + metric_results.name + ' by Industry'
		else:
			grouping_ids, categories = zip(*self._get_region_grouping_ids(regions_dic['id']))
			self.xAxis['title'] = 'Region'
			self.title = 'Distribution of ' + portfolio_name + ' ' + metric_results.name + ' by Geography'

		self.yAxis['title'] = metric_results.name + " (" + metric_results.provider + ")"

		# demonstrate the portfolio have missing data for categories, 
		# any portfolio has completed data(missing_categories = False), we will show all categories
		completed_categories = False

		ids_set = set()
		raw_data = []

		for portfolio in portfolios:
			portfolio_data = {}
			try:
				date = get_last_available_day_until_date_in_grouping_metric(date_parameters, portfolio, grouping_ids).strftime("%Y-%m-%d")
				portfolio_grouping_metric_result = PortfolioGroupingMetricModel.query.\
								filter_by(metric_id = metric[0]['id']).\
								filter(PortfolioGroupingMetricModel.grouping_id.in_(grouping_ids)).\
								join(PortfolioGroupingMetricModel.portfolio_metric_date).\
								filter_by(portfolio_id = portfolio['id']).\
								filter_by(date_key = date).\
								order_by(PortfolioGroupingMetricModel.grouping_id.asc()).all()

				portfolio_data['name'] = portfolio['name'] + ' (' + str(date) + ')'

				temp_portfolio_grouping_metric_results = [(portfolio_grouping_metric.grouping_id, portfolio_grouping_metric.value) for portfolio_grouping_metric in portfolio_grouping_metric_result]
				exist_grouping_ids, values = zip(* temp_portfolio_grouping_metric_results)
				ids_set = ids_set.union(set(exist_grouping_ids))
				portfolio_data['data'] = dict(zip(exist_grouping_ids,values))

			except:
				portfolio_data['name'] = portfolio['name']
				portfolio_data['data']  = {}

			raw_data.append(portfolio_data)

		ordered_ids, modified_categories = zip(* self._get_exist_grouping_ids_and_names(ids_set))

		self.xAxis['categories'] = list(modified_categories)

		for data in raw_data:
			processed_portfolio_data = {'name':data['name'], 'data':[]}
			for id in ordered_ids:
				processed_portfolio_data['data'].append(data['data'].get(id, 0))
			self.data.append(processed_portfolio_data)

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
