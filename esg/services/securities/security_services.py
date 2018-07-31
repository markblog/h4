from esg.models.security_contribution_model import SecurityContributionModel
from ext import db

def get_last_available_day_until_date_in_security_contribution(date_parameters, portfolio_id, grouping_id):
	latest_date = SecurityContributionModel.query.filter_by(portfolio_id = portfolio_id).\
															filter_by(grouping_id = grouping_id).\
															filter(SecurityContributionModel.date_key <= date_parameters).\
															order_by(SecurityContributionModel.date_key.desc()).\
															first()

	return latest_date.date_key