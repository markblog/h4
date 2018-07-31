from esg.models.charts.line_chart import LineChart
from esg.models.esg_factor_model import EsgFactorModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.grouping_model import GroupingModel
from esg.models.portfolio_metric_date_model import PortfolioMetricDateModel
from esg.services.charts.charting_rules import TagTypeChart
from esg.services.charts.portfolio_time_frequency import PortfolioGroupingTimeFrequency
from ext import db


class MultipleRegionSectorEsgScoreTimeSeries(LineChart):
    """
    This is for chart twelve
    """

    def __init__(self):
        super().__init__()
        self.title = 'time series'
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
        either_parameters = [TagTypeChart.REGION, TagTypeChart.SECTOR]
        number_of_parameters = [(TagTypeChart.ESG_METRICS, 1)]
        return[(required_parameters, either_parameters, number_of_parameters)]

    def _parse_parameters(self, parameters_dic):
        self._parameters = parameters_dic

    def fetch_data(self, **kwargs):
        self._parse_parameters(kwargs['parameters_dic'])
        portfolios_value = self._parameters.get(TagTypeChart.PORTFOLIO)
        frequency = self._parameters.get(TagTypeChart.TIME)[0]['id']
        weight_method_value = self._parameters.get(TagTypeChart.WEIGHT_METHOD)
        esg_factors_value = self._parameters.get(TagTypeChart.ESG_METRICS)
        region_value = self._parameters.get(TagTypeChart.REGION, None)
        sector_value = self._parameters.get(TagTypeChart.SECTOR, None)

        zipped_list = []
        union_set = set()
        values = []
        date_list = self.get_datelist_for_portfolio(frequency, portfolios_value[0]['id'])
        esg_factor_id, provider_name = self._get_esg_id_and_name(esg_factors_value[0]['id'])

        if not self._is_empty(region_value):
            values = region_value
            self.title = portfolios_value[0]['name'] + ' ' + esg_factors_value[0]['name'] + ' in Multiple Regions Time Series'
            grouping_ids, names = zip(*self._get_region_grouping_ids(region_value))
        elif not self._is_empty(sector_value):
            values = sector_value
            self.title = portfolios_value[0]['name'] + ' ' + esg_factors_value[0]['name'] + ' in Multiple Sectors Time Series'
            grouping_ids, names = zip(*self._get_sector_grouping_ids(sector_value))
        elif not (self._is_empty(sector_value))and not (self._is_empty(region_value)):
            self.title = portfolios_value[0]['name'] + ' ' + esg_factors_value[0]['name'] + ' in '+ region_value[0]['name'] +'in '+sector_value[0][' name']+' Time Series'
            grouping_ids, names = zip(*self._get_region_sector_grouping_ids(sector[0]['id'], region[0]['id']))

        for grouping_id in grouping_ids:
            sql = 'SELECT value,date_key FROM ' + \
                    '(SELECT portfolio_metric_date_id, metric_id, grouping_id, value FROM public.portfolio_grouping_metric ' + \
                    'WHERE portfolio_metric_date_id in (SELECT id FROM public.portfolio_metric_date WHERE portfolio_id = '+ str(portfolios_value[0]['id'])+') ' + \
                    'AND grouping_id = '+str(grouping_id)+' AND metric_id = '+ str(esg_factor_id) +') t ' + \
                    'LEFT JOIN public.portfolio_metric_date pmd ON t.portfolio_metric_date_id = pmd.id ORDER BY date_key ASC'
            metric_results = db.engine.execute(sql)

            portfolio_dic = {portfolio.date_key.strftime("%Y-%m-%d"): portfolio.value for portfolio in metric_results}
            zipped_list.append(portfolio_dic)
            union_set = union_set.union(portfolio_dic.keys())

        for index, region in enumerate(values):
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
            portfolio_data['name'] = region['name']
            portfolio_data['data'] = data_list
            self.data.append(portfolio_data)

        self.xAxis['categories'] = union_list
        self.xAxis['title'] = 'Time series'
        self.yAxis['title'] = esg_factors_value[0]['name'] + ' (' + provider_name + ')'

    def get_datelist_for_portfolio(self, frequency, portfolio):

        time_frequency = PortfolioGroupingTimeFrequency()

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

    def _get_region_grouping_ids(self,geography_value):
        geography_ids=[geography['id'] for geography in geography_value]
        grouping_results = GroupingModel.query \
                .filter(GroupingModel.geography_id.in_(geography_ids))\
                .filter(GroupingModel.sector_id == None).all()
        ids = [(grouping.id, grouping.name) for grouping in grouping_results]
        return ids

    def _get_sector_grouping_ids(self,sector_value):
        sector_ids=[sector['id'] for sector in sector_value]
        grouping_results = GroupingModel.query\
                        .filter(GroupingModel.sector_id.in_(sector_ids))\
                        .filter(GroupingModel.geography_id == None).all()
        ids = [(grouping.id, grouping.name) for grouping in grouping_results]
        return ids

    def _get_region_sector_grouping_ids(self,geography_id, sector_id):
        grouping_results = GroupingModel.query \
                            .filter(GroupingModel.sector_id == sector_id,\
                                GroupingModel.region_id == geography_id).all()
        ids = [(grouping.id, grouping.name) for grouping in grouping_results]
        return ids
