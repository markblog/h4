from esg.models.charts.donut_chart import DonutChart
from esg.models.exceptions.custom_exceptions import ESGException
from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
# from esg.services.portfolios.portfolio_service import get_last_available_day_until_date_in_grouping_metric
from esg.services.charts.charting_rules import TagTypeChart
from ext import db


class AllESGScoresForPortfolioOrSecurity(DonutChart):
	def __init__(self):
		super().__init__()
		self.title = 'All ESG scores for a portfolio or security'
		self.subtitle = 'State Street'
		self.data = []

	@staticmethod
	def parameter_settings():
		required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.DETAILS, TagTypeChart.WEIGHT_METHOD,
							   TagTypeChart.DATE]
		number_of_parameters = [(TagTypeChart.PORTFOLIO, 1)]

		return [(required_parameters, None, number_of_parameters)]

	def _parse_parameters(self, parameters_dic):
		self._parameters = parameters_dic

	def fetch_data(self, **kwargs):

		self._parse_parameters(kwargs['parameters_dic'])

		portfolio = self._parameters.get(TagTypeChart.PORTFOLIO)
		detail = self._parameters.get(TagTypeChart.DETAILS)
		date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']
		date = self._get_last_evaluate_day_until_date(date_parameters, portfolio[0]).strftime("%Y-%m-%d")

		self.subtitle = 'Source date: ' + str(date)

		if detail[0]['id'] == 20:
			self.data_provider = 'AE'
			self.title = 'Arabesque ESG Score Details of ' + portfolio[0]['name']
		elif detail[0]['id'] == 21:
			self.data_provider = 'AU'
			self.title = 'Arabesque UNGC Score Details of ' + portfolio[0]['name']
		else:
			print('Not support data provider in this version')

		portfolio_esg_score_sql = "SELECT * FROM " + \
								  "(SELECT esg_factor_id, score FROM public.portfolio_esg_score WHERE date_key = '" + date + "' AND portfolio_id = " + str(
			portfolio[0]['id']) + ") t " + \
								  "LEFT JOIN public.esg_factor ef ON t.esg_factor_id = ef.id " + \
								  "WHERE data_provider_id = '" + self.data_provider + "' ORDER BY level ASC"

		portfolio_esg_score_results = db.engine.execute(portfolio_esg_score_sql)

		self.data = self._parse_esg_results(portfolio_esg_score_results)

	def _get_last_evaluate_day_until_date(self, date, portfolio):
		# To comment here
		available_date = None
		all_date_list = db.session.query(PortfolioEsgScoreModel.date_key). \
			distinct(). \
			filter_by(portfolio_id=portfolio['id']). \
			filter(PortfolioEsgScoreModel.date_key <= date). \
			order_by(PortfolioEsgScoreModel.date_key.desc()). \
			all()

		if len(all_date_list) > 0:
			available_date = all_date_list[0][0]
		else:
			raise ESGException('Can not find the data for ' + portfolio['name'] + ' before the ' + str(date))

		return available_date

	def _parse_esg_results(self, esg_resulsts):

		class Node():
			def __init__(self, data):
				self.id = data.id
				self.name = data.name
				self.level = data.level
				self.score = data.score
				self.parent_id = data.parent_id
				self.weight = 1

			def add_child(self, node):
				if not hasattr(self, 'children'):
					self.children = []

				self.children.append(node)

			def search(self, id):
				if self.id == id:
					return self
				elif hasattr(self, 'children'):
					for child in self.children:
						if child.id == id:
							return child
						else:
							child.search(id)
				else:
					return None

			def allocate_weight(self):
				if hasattr(self, 'children'):
					for child in self.children:
						child.weight = self.weight / len(self.children)
						child.allocate_weight()

			def to_dict(self):
				if hasattr(self, 'children'):
					temp_list = []
					for child in self.children:
						dic = child.to_dict()
						if dic:
							temp_list.append(dic)
					self.children = temp_list
					return self.__dict__
				else:
					self.children = []
					return self.__dict__

		root = None

		for index, result in enumerate(esg_resulsts):
			if index == 0:
				root = Node(result)
			else:
				child = Node(result)
				parent = root.search(child.parent_id)
				if parent:
					parent.add_child(child)
				else:
					print('Can not find the parent of this node, please check!')
		if not root:
			raise ESGException('No data available for this chart')

		root.allocate_weight()
		root.to_dict()
		root.parent_id = 0
		return root.__dict__
