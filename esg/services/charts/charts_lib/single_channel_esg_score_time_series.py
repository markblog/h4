from esg.models.charts.line_chart import LineChart
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.charts.portfolio_time_frequency import PortfolioTimeFrequency
from ext import db


class SingleChannelEsgScoreTimeSeries(LineChart):
    """
	This is for chart five
	"""

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
        self.data = []

    @staticmethod
    def parameter_settings():
        required_parameters = [TagTypeChart.PORTFOLIO,TagTypeChart.ESG_METRICS, TagTypeChart.TIME, TagTypeChart.WEIGHT_METHOD]
        number_of_parameters = [(TagTypeChart.ESG_METRICS, 1)]

        return[(required_parameters, None, number_of_parameters)]

    def _parse_parameters(self, parameters_dic):
        self._parameters = parameters_dic

    def fetch_data(self, **kwargs):

        self._parse_parameters(kwargs['parameters_dic'])

        portfolios_value = self._parameters.get(TagTypeChart.PORTFOLIO)
        frequency = self._parameters.get(TagTypeChart.TIME)[0]['id']
        weight_method_value = self._parameters.get(TagTypeChart.WEIGHT_METHOD)
        esg_factors_value = self._parameters.get(TagTypeChart.ESG_METRICS)

        esg_factor_id, provider_name = self._get_esg_id_and_name(esg_factors_value[0]['id'])
        if len(portfolios_value) > 1:
            self.title = 'Multiple portfolios ' + esg_factors_value[0]['name'] + ' Time Series'
        else:
            self.title = portfolios_value[0]['name'] + ' ' + esg_factors_value[0]['name'] + ' Time Series'
        zipped_list = []
        union_set = set()
        for portfolio in portfolios_value:
            date_list = self.get_datelist_for_portfolio(frequency, portfolio['id'])
            scores = PortfolioEsgScoreModel.query \
                .filter_by(portfolio_id=portfolio['id']) \
                .filter_by(weight_method=weight_method_value[0]['id']) \
                .filter(PortfolioEsgScoreModel.esg_factor_id == esg_factor_id,
                        PortfolioEsgScoreModel.date_key
                        .in_(date_list)).order_by(PortfolioEsgScoreModel.date_key.asc()).all()
            portfolio_dic = {portfolio.date_key.strftime("%Y-%m-%d"): portfolio.score for portfolio in scores}
            zipped_list.append(portfolio_dic)
            union_set = union_set.union(portfolio_dic.keys())

        for index, portfolio in enumerate(portfolios_value):
            portfolio_data = {}
            temp_dic = zipped_list[index]
            union_list = list(union_set)
            union_list.sort()
            data_list = []
            for date in union_list:
                if date not in temp_dic.keys():
                    data_list.append(None)
                else:
                    data_list.append(temp_dic.get(date))
            portfolio_data['name'] = portfolio['name']
            portfolio_data['data'] = data_list
            self.data.append(portfolio_data)
        self.xAxis['categories'] = union_list
        self.xAxis['title'] = 'Time series'
        self.yAxis['title'] = esg_factors_value[0]['name'] + ' (' + provider_name + ')'

    def get_datelist_for_portfolio(self, frequency, portfolio):

        time_frequency = PortfolioTimeFrequency()

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
