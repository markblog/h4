from esg.models.charts.bar_chart import BarChart
from esg.models.exceptions.custom_exceptions import ESGException
from esg.models.portfolio_result_model import PortfolioResultModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric
from esg.models.metric_model import MetricModel
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_portfolio_metric


class PortfolioMetricHistogram(BarChart):
    def __init__(self):
        super().__init__()
        self.title = ''
        self.subtitle = 'State Street'
        self.xAxis = {
            "categories": []
        }
        self.yAxis = {}
        self.data = []
        self._parameters = {}
        self._value_dic = {'Cumulative Return': 'Cumulative Return',
                  'Return (daily)': 'Return Daily',
                  'Market Value': 'Market Value',
                  'Number of securities': 'Number of Securities',
                  }

    @staticmethod
    def parameter_settings():
        _required_parameters = [TagTypeChart.PORTFOLIO, TagTypeChart.PORTFOLIO_METRICS,TagTypeChart.DATE]
        _number_of_parameters = [(TagTypeChart.PORTFOLIO_METRICS, 1)]

        return [(_required_parameters, None, _number_of_parameters)]

    def _parse_parameters(self, parameters_dic):
        self._parameters = parameters_dic

    def fetch_data(self, **kwargs):
        self._parse_parameters(kwargs['parameters_dic'])
        self._get_available_chart_type()
        portfolios = self._parameters.get(TagTypeChart.PORTFOLIO)
        market_list = self._parameters.get(TagTypeChart.PORTFOLIO_METRICS)
        date_parameters = self._parameters.get(TagTypeChart.DATE)[0]['name']

        for market in market_list:
            market_key = market['name']
            market_list_para = [value for key, value in self._value_dic.items() if key == market_key]
            metric_num = MetricModel.query.filter(MetricModel.name == market_list_para[0]).all()
            metric_id = [model.id for model in metric_num]
            
        portfolio_names = []
        for portfolio in portfolios:
            date = get_last_available_day_until_date_in_portfolio_metric(date_parameters, portfolio['id']).strftime("%Y-%m-%d")
            model_results = PortfolioResultModel.query.\
            filter_by(portfolio_id=portfolio['id']).\
            filter_by(date_key=date).\
            all()

            metric_data = []
            if market_key == 'Cumulative Return':
                metric_data = [model.cumulative_return for model in model_results]
            elif market_key == 'Return (daily)':
                metric_data = [model.return_daily for model in model_results]    
            elif market_key == 'Number of securities':
                metric_data = [model.number_securities for model in model_results]  
            elif market_key == 'Market Value':
                metric_data = [model.market_value for model in model_results]  
                
            data ={}
            data['name'] = portfolio['name']+" "+"("+date+")"
            data['data'] = metric_data
            self.data.append(data)
            self.title = portfolio['name'] +"'s"+' '+market_key
            portfolio_names.append(portfolio['name'])
        if len(portfolios) > 1:
            self.title = "Multiple portfolio's"+' '+market_key
        self.yAxis['title'] = market_key
        self.xAxis['categories'] = ' '

    def _get_available_chart_type(self):
        print(self._parameters)
        if len(self._parameters.get(TagTypeChart.PORTFOLIO)) == 1:
            self.available_chart_type = {
                            'bar': 'bar',
                            'radar':'radar',
                            'pie':'pie'
                        }
        else:
            self.available_chart_type = {
                            'bar': 'bar',
                            'stackedBar':'stacked bar',
                            'stackedPercentageBar':'stacked percentage bar',
                            'radar':'radar'
                        }