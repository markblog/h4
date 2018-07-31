from esg.models.portfolio_esg_score_model import PortfolioEsgScoreModel
from esg.services.charts.time_frequency import TimeFrequency
from esg.models.portfolio_result_model import PortfolioResultModel
from esg.models.portfolio_metric_date_model import PortfolioMetricDateModel

from ext import db


class PortfolioTimeFrequency(TimeFrequency):
    def _all_date(self, *para):
        """
          get the date list of whole portfolio order by date descend
          """
        if para is not None and para != ():
            if para[0] != 0:
                all_date_list = db.session.query(PortfolioEsgScoreModel.date_key). \
                    filter_by(portfolio_id=para[0]). \
                    distinct(). \
                    order_by(PortfolioEsgScoreModel.date_key.desc()). \
                    all()
            else:
                all_date_list = db.session.query(PortfolioEsgScoreModel.date_key) \
                    .filter(PortfolioEsgScoreModel.esg_factor_id == para[1]).\
                    distinct(). \
                    order_by(PortfolioEsgScoreModel.date_key.desc()). \
                    all()

        else:
            all_date_list = db.session.query(PortfolioEsgScoreModel.date_key). \
                distinct(). \
                order_by(PortfolioEsgScoreModel.date_key.desc()). \
                all()

        return all_date_list

class PortfolioMetricTimeFrequency(TimeFrequency):
    def _all_date(self, *para):
        """
          get the date list of whole portfolio order by date descend
          """
        if para is not None and para != ():
            if para[0] != 0:
                all_date_list = db.session.query(PortfolioResultModel.date_key). \
                    filter_by(portfolio_id=para[0]). \
                    distinct(). \
                    order_by(PortfolioResultModel.date_key.desc()). \
                    all()
            else:
                all_date_list = db.session.query(PortfolioResultModel.date_key) \
                    .filter(PortfolioResultModel.portfolio_id == para[1]).\
                    distinct(). \
                    order_by(PortfolioResultModel.date_key.desc()). \
                    all()

        else:
            all_date_list = db.session.query(PortfolioResultModel.date_key). \
                distinct(). \
                order_by(PortfolioResultModel.date_key.desc()). \
                all()

        return all_date_list
        
class PortfolioGroupingTimeFrequency(TimeFrequency):
    def _all_date(self, *para):
        """
          get the date list of whole portfolio order by date descend
          """
        if para is not None and para != ():
            if para[0] != 0:
                all_date_list = db.session.query(PortfolioMetricDateModel.date_key). \
                    filter_by(portfolio_id=para[0]). \
                    distinct(). \
                    order_by(PortfolioMetricDateModel.date_key.desc()). \
                    all()
            else:
                all_date_list = db.session.query(PortfolioMetricDateModel.date_key) \
                    .filter(PortfolioMetricDateModel.portfolio_id == para[1]).\
                    distinct(). \
                    order_by(PortfolioMetricDateModel.date_key.desc()). \
                    all()

        else:
            all_date_list = db.session.query(PortfolioMetricDateModel.date_key). \
                distinct(). \
                order_by(PortfolioMetricDateModel.date_key.desc()). \
                all()

        return all_date_list
