from esg.models.portfolio_metric_date_model import PortfolioMetricDateModel
from esg.models.portfolio_grouping_metric_model import PortfolioGroupingMetricModel
from esg.models.portfolio_security_model import PortfolioSecurityModel
from esg.models.exceptions.custom_exceptions import ESGException
from esg.models.portfolio_result_model import PortfolioResultModel
from ext import db


# Here may be a class later
def get_last_available_day_until_date_in_grouping_metric(date, portfolio, grouping_ids):
		# get the date which have the data for charting before the date is inputed by user
		available_date = None
		all_date_list = db.session.query(PortfolioMetricDateModel.date_key).\
                                    filter_by(portfolio_id = portfolio['id']).\
                                    filter(PortfolioMetricDateModel.date_key <= date).\
                                    distinct().\
                                    join(PortfolioGroupingMetricModel).\
                                    filter(PortfolioGroupingMetricModel.grouping_id.in_(grouping_ids)).\
                                    order_by(PortfolioMetricDateModel.date_key.desc()).\
                                    first()

		if all_date_list is not None and len(all_date_list) > 0:
			available_date = all_date_list[0]
		else:
			raise ESGException('Can not find the data for ' + portfolio['name'] + ' before the ' + str(date))

		return available_date

def get_portfolio_latest_updated_date(date, portfolio_id):
		# Here we use the latest before the last transaction day or just use the portfolio before the input date
		latest_updated_date = PortfolioSecurityModel.query.filter_by(portfolio_id = portfolio_id).\
															filter(PortfolioSecurityModel.portfolio_update_date <= date).\
															order_by(PortfolioSecurityModel.portfolio_update_date.desc()).\
															first()

		return latest_updated_date.portfolio_update_date

def get_last_available_day_until_date_in_portfolio_metric(date, portfolio_id):
        # Here we use the latest before the last transaction day or just use the portfolio before the input date
        latest_updated_date = PortfolioResultModel.query.filter_by(portfolio_id = portfolio_id).\
                                                            filter(PortfolioResultModel.date_key <= date).\
                                                            order_by(PortfolioResultModel.date_key.desc()).\
                                                            first()
        return latest_updated_date.date_key


# def _get_all_sector_ids_by_level(portfolio_id,level,date):

# 	portfolio_security_results = PortfolioSecurityModel.query.filter_by(portfolio_id = portfolio_id).\
# 															filter(PortfolioSecurityModel.portfolio_update_date <= date).\

# 	sector_results = SectorModel.query.filter_by(level = level).all()
# 	sector_ids = [sector.id for sector in sector_results]
# 	return sector_ids

# def _get_all_region_ids_by_level(portfolio_id,level,date):
# 	geography_results = GeographyModel.query.filter_by(level=level).all()
# 	geography_ids = [geography.id for geography in geography_results]
# 	return geography_ids