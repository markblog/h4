from enum import Enum

class ESGException(Exception):

	def __init__(self, message):
		super().__init__()
		self.message = message


class TagTypeChart(Enum):
	PORTFOLIO = 1
	ESG_METRICS = 2
	PORTFOLIO_METRICS = 3
	REGION = 4
	SECTOR = 5
	TIME = 6
	REPORTING_SCOPE = 7
	WEIGHT_METHOD = 8
	CONTROL = 9
	DETAILS = 10 # 10,11,12 is generated from Reporting_scope
	ALL_REGIONS_SECTORS = 11
	ALL_SECURITIES = 12
	DATE = -1
	BUCKETS = -2
	WEIGHT = -3

class NoDataException(ESGException):

	def __init__(self):
		super().__init__('No data available for this chart')

if __name__ == '__main__':
	print(TagTypeChart.PORTFOLIO)
