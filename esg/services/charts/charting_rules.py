from collections import defaultdict
from esg.models.exceptions.custom_exceptions import ESGException


class TagTypeChart:
    PORTFOLIO = 1
    ESG_METRICS = 2
    PORTFOLIO_METRICS = 3
    REGION = 4
    SECTOR = 5
    TIME = 6
    REPORTING_SCOPE = 7
    WEIGHT_METHOD = 8
    CONTROL = 9
    DETAILS = 10  # 10,11,12 is generated from Reporting_scope
    ALL_REGIONS_SECTORS = 11
    ALL_SECURITIES = 12
    ALL_CONTRIBUTORS = 13

    ANALYSIS = 100
    GLOBAL_MAP = 101
    MARGINAL_CONTRIBUTION = 102

    DATE = -1
    BUCKETS = -2
    WEIGHT = -3


TagTypeChart_dic = {
    1: 'portfolio',
    2: 'esg metrics',
    3: 'portfolio metrics',
    4: 'region',
    5: 'sector',
    6: 'time',
    7: 'reporting scope',
    8: 'weight method',
    9: 'control',
    10: 'details(esg/ungc)',
    11: 'all regions and sectors',
    12: 'all securities',
    13: 'contributors',
    100: 'analysis',
    101: 'global map',
    102: 'marginal contribution',
    -1: 'date',
    -2: 'buckets',
    -3: 'weight method'
}


class ChartingRules():
    def __init__(self, parameters):
        self.required_parameters = None
        self.either_parameters = None
        self.number_of_parameters = None
        self.error_message = None
        self.scores = 0
        self.dic = defaultdict(list)
        self._get_tags_dic_by_type(parameters)

    def _get_tags_dic_by_type(self, parameters):

        for tag in parameters:
            self.dic[tag['tag_type_id']].append(tag)

        for tag in self.dic.get(7, []):
            if tag['id'] == 1:
                self.dic[12].append(tag)
            elif tag['id'] in [2, 3, 4, 5]:
                self.dic[11].append(tag)
            elif tag['id'] in [20, 21]:
                self.dic[10].append(tag)
            elif tag['id'] in [6]:
                self.dic[13].append(tag)
            else:
                print('The other scopes here, we will not process')

        for tag in self.dic.get(9, []):
            if tag['id'] == 1:
                self.dic[100].append(tag)
            elif tag['id'] == 2:
                self.dic[101].append(tag)
            elif tag['id'] in [100,101]:
                self.dic[102].append(tag)
            else:
                print('The other scopes here, we will not process')

        self.dic.pop(7, None)
        self.dic.pop(9, None)

    # print(self.dic)

    def _check_tag_type_for_routing(self, required_parameters, either_parameters, number_of_parameters):
        """
		args:
			required_parameters: need for each chart
			either_parameters: either parameters show up is OK, but only one
			number_of_parameters: define the number of parameters should have in required_parameters
		"""
        flag = True
        full_set = [-1, -2, -3, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        number_of_element_in_either_parameters = 0
        right_tags = 0  # the number of right tags for each chart, for ranking the closest chart when we give the error message
        error_message = ''  # error message we want to give the user

        # required_parameters, either_parameters, number_of_parameters = parameters_tuple

        # conver the tuple list to the dictionary
        if number_of_parameters:
            number_of_parameters_dic = {item[0]: item[1] for item in number_of_parameters}

        for item in required_parameters:
            if item in self.dic.keys():
                if number_of_parameters and item in number_of_parameters_dic.keys():
                    if number_of_parameters_dic[item] < len(self.dic[item]):
                        error_message = 'Too many ' + TagTypeChart_dic.get(item) + ' tags were selected for this chart (' +str(number_of_parameters_dic[item])+' allowed)'
                        flag = False
                        break
                    elif number_of_parameters_dic[item] > len(self.dic[item]):
                        error_message = 'Not enough ' + TagTypeChart_dic.get(item) + ' tags were selected for this chart (' + str(number_of_parameters_dic[item]) + ' needed)'
                        flag = False
                        break
                    else:
                        right_tags += 1
            else:
                flag = False
                error_message = 'Missing required ' +TagTypeChart_dic.get(item) + ' tag(s)'
                break

        if either_parameters:
            for item in either_parameters:
                if item in self.dic.keys():
                    if number_of_parameters and item in number_of_parameters_dic.keys():
                        if number_of_parameters_dic[item] != len(self.dic[item]):
                            error_message = 'The number of ' + TagTypeChart_dic.get(
                                item) + " tags (" + str(len(self.dic[item])) + ") doesn't match the number we expected (" + str(
                                number_of_parameters_dic[item]) + ") for this chart"
                            flag = False
                            break
                        else:
                            right_tags += 1

                    number_of_element_in_either_parameters += len(self.dic[item])

            if number_of_element_in_either_parameters == 0:
                error_message = 'Please select one of the follwing tags: ['
                for index, item in enumerate(either_parameters):
                    error_message += TagTypeChart_dic.get(item)
                    if index != len(either_parameters):
                        error_message += ','
                error_message += ']'

                flag = False

            should_empty_list = [item for item in full_set if
                                 (item not in required_parameters) and (item not in either_parameters)]
        else:
            should_empty_list = [item for item in full_set if (item not in required_parameters)]

        for item in should_empty_list:
            if self.dic.get(item, None):
                error_message = 'Error: Unexpected ' + TagTypeChart_dic.get(item) + ' tag. Please remove and try again.'
                flag = False
            else:
                right_tags += 1

        # simple method to determine chart that user want to charting, and give the error message
        if not flag and right_tags / 15 > self.scores:
            self.scores = right_tags / 15
            self.error_message = error_message

        return flag

    def check_parameters(self, parameters):
        for parameter in parameters:
            required_parameters, either_parameters, number_of_parameters = parameter
            if self._check_tag_type_for_routing(required_parameters, either_parameters, number_of_parameters):
                return True
        return False
