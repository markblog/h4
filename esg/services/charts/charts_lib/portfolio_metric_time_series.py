from esg.models.charts.bar_chart import BarChart
from esg.models.exceptions.custom_exceptions import ESGException
from esg.models.portfolio_result_model import PortfolioResultModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.portfolios.portfolio_services import get_last_available_day_until_date_in_grouping_metric
from esg.models.metric_model import MetricModel
from esg.models.charts.line_chart import LineChart
from esg.services.charts.portfolio_time_frequency import PortfolioMetricTimeFrequency

class PortfolioMetricTimeSeries(LineChart):

    def __init__(self):
        super().__init__()
        self.title = 'Performance by single-channel ESG score time series'
        self.subtitle = 'State Street'
        self.xAxis = {
            "categories": [
                "0 - 10",
                "10 - 20",
                "20 - 30",
                "30 - 40",
                "40 - 50",
                "50 - 60",
                "60 - 70",
                "70 - 80",
                "80 - 90",
                "90 - 100"
            ]
        }
        self.yAxis = {"title": "portfolio value"}
        self._value_dic = {'Cumulative Return': 'Cumulative Return',
          'Return (daily)': 'Return Daily',
          'Market Value': 'Market Value',
          'Number of securities': 'Number of Securities',
          }

        self.data = []

    @staticmethod
    def parameter_settings():
        required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.PORTFOLIO_METRICS, TagTypeChart.TIME]
        number_of_parameters = [(TagTypeChart.PORTFOLIO_METRICS, 1)]

        return[(required_parameters, None, number_of_parameters)]

    def _parse_parameters(self, parameters_dic):
        self._parameters = parameters_dic

    def fetch_data(self, **kwargs):
        metric_data = {}
        self._parse_parameters(kwargs['parameters_dic'])
        portfolios = self._parameters.get(TagTypeChart.PORTFOLIO)
        market_list = self._parameters.get(TagTypeChart.PORTFOLIO_METRICS)
        frequency = self._parameters.get(TagTypeChart.TIME)[0]['id']

        for market in market_list:
            market_key = market['name']
            market_list_para = [value for key, value in self._value_dic.items() if key == market_key]
            metric_num = MetricModel.query.filter(MetricModel.name == market_list_para[0]).all()
            metric_id = [model.id for model in metric_num]


        for portfolio in portfolios:
            date_list = self.get_datelist_for_portfolio(frequency, portfolio['id'])
            model_results = PortfolioResultModel.query.\
                filter_by(portfolio_id=portfolio['id']).\
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

            poerfolio_metric_data={}

            poerfolio_metric_data['name'] = portfolio['name']
            poerfolio_metric_data['data'] = metric_data
            self.data.append(poerfolio_metric_data)

            self.yAxis['title'] = market_key
            self.title = portfolio['name'] + ' ' + market_key +' Time Series'
            self.xAxis['categories'] = date_list

        if len(portfolios) > 1:
            self.title = 'Multiple Portfolio Metric Time Series'



    def get_datelist_for_portfolio(self, frequency, portfolio):

        time_frequency = PortfolioMetricTimeFrequency()

        if frequency == 4: # weekly
            date_list = time_frequency._is_last_transaction_day_of_a_week(portfolio)
        elif frequency == 3: # monthly
            date_list = time_frequency._is_last_transaction_day_of_a_month(portfolio)
        elif frequency == 2: # quarterly
            date_list = time_frequency._is_last_transaction_day_of_a_quarter(portfolio)
        elif frequency == 1: # yearly
            date_list = time_frequency._is_last_transaction_day_of_a_year(portfolio)
        else:
            date_list = time_frequency._all_date(portfolio)
            date_list = [date.date_key.strftime('%Y-%m-%d') for date in date_list]
        date_list.reverse()
        return date_list












    def get_datelist_for_portfolio(self, frequency, portfolio):

        time_frequency = PortfolioMetricTimeFrequency()

        if frequency == 4: # weekly
            date_list = time_frequency._is_last_transaction_day_of_a_week(portfolio)
        elif frequency == 3: # monthly
            date_list = time_frequency._is_last_transaction_day_of_a_month(portfolio)
        elif frequency == 2: # quarterly
            date_list = time_frequency._is_last_transaction_day_of_a_quarter(portfolio)
        elif frequency == 1: # yearly
            date_list = time_frequency._is_last_transaction_day_of_a_year(portfolio)
        else:
            date_list = time_frequency._all_date(portfolio)
            date_list = [date.date_key.strftime('%Y-%m-%d') for date in date_list]
        date_list.reverse()
        return date_list

    def _get_esg_id_and_name(self, esg_factor_id):
        esg_factor_results = EsgFactorModel.query.filter_by(id=esg_factor_id).first()
        return esg_factor_results.id, esg_factor_results.data_provider.name
