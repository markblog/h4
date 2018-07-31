from flask import jsonify
from operator import itemgetter

class BaseChart(object):

	def __init__(self):
		self.title = 'chart'
		self.subtitle = 'subtitle'
		self.type='type'
		self.data = []
		self.available_chart_type = []

	def as_dict(self):
		"""
		generate the dictionary that didn't include the variables which starts with '_'
		this dictionary is used to sent to the front-end as json object
		"""
		dic = {}

		for key, value in self.__dict__.items():
			if not key.startswith('_'): 
				dic[key] = value

		return dic

	def to_json(self):
		return jsonify(self.as_dict)

	def _parse_parameters_dic_to_list(self, parameter_list):

		result_dict = {}

		if len(parameter_list) > 0:
			for key in parameter_list[0].keys():
				result_dict[key] = []

			for item in parameter_list:
				for key,value in item.items():
					result_dict[key].append(value)
		
		else:
			result_dict = None

		return result_dict

	def _is_empty(self, parameters_list):
		return parameters_list is None or len(parameters_list) == 0
		
	@staticmethod
	def parameter_settings():
		"""
		define the parameter requriments of each chart
		"""
		raise "Not Implemented"

	def _parse_parameters(self,json):
		raise "Not Implemented"

	def fetch_data(self, **kwargs):
		raise "Not Implemented"

	def check_parameters(self,**kwargs):
		raise "Not Implemented"

	def _get_available_chart_type(self):
		raise "No Implemented"
