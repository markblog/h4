# Add your blueprint here
from application import app, api

from esg import app_esg

# auth
from esg.resources.auth_resource import UserLogon, UserLogoff, UserProfile
# alert
from esg.resources.alert_type_resource import AlertList, AlertMarkRead, AlertMarkAllRead, AlertDismiss, AlertDismissAll
# portfolio
from esg.resources.portfolio_resource import PortfolioModelList
from esg.resources.tag_history_resource import TagHistory
from esg.resources.tag_type_resource import TagsByTags
from esg.resources.esg_charts_resource import EsgChartsRouting
# company
from esg.resources.data_provider_resource import DataProviderList
from esg.resources.company_resource import CompanyList, CompanyESGSummary
# data management
from esg.resources.data_management_resource import PortfolioDataManager

app.register_blueprint(app_esg.bp)
# api.add_resource(NoteResource, '/api/note', '/api/note/<keyword>')

# authorization api
api.add_resource(UserLogon, '/api/auth/logon')
api.add_resource(UserLogoff, '/api/auth/logoff')
api.add_resource(UserProfile, '/api/auth/user_profile')

# portfolio api
api.add_resource(PortfolioModelList, '/api/portfolio/list')
api.add_resource(TagHistory, '/api/tags/tag_history')
api.add_resource(TagsByTags, '/api/tags/by_tags')
api.add_resource(EsgChartsRouting, '/api/esg_charts')
# company api
api.add_resource(DataProviderList, '/api/data_provider_list')
api.add_resource(CompanyList, '/api/company_list')
api.add_resource(CompanyESGSummary, '/api/company_esg_summary/<data_provider_id>/<company_id>')
api.add_resource(CompanyESGSummary, '/api/company_esg_summary', endpoint='default')
# data management api
api.add_resource(PortfolioDataManager, '/api/data_management/portfolio/upload', endpoint='upload_portfolio')
api.add_resource(PortfolioDataManager, '/api/data_management/portfolio/download/<file_name>', endpoint='download_portfolio')
#alerts api
api.add_resource(AlertList, '/api/alert/list')
api.add_resource(AlertMarkRead, '/api/alert/<alert_history_id>/mark_read')
api.add_resource(AlertMarkAllRead, '/api/alert/mark_all_read')
api.add_resource(AlertDismiss, '/api/alert/<alert_history_id>/dismiss')
api.add_resource(AlertDismissAll, '/api/alert/dismiss_all')


# api.add_resource(PortfolioDataManager, '/api/data_management/download/portfolio')
# api.add_resource(PortfolioDataManager, '/api/data_management/portfolio')
# api.add_resource(ChartFromTags, '/api/chart/from_tags')
# api.add_resource(PortfolioTags, '/api/portfolio/tags')
# api.add_resource(Charting, '/api/chart')
# api.add_resource(ESGSummary, '/api/esg_summary/<company_id>')
# api.add_resource(ESGSummaryChart, '/api/esg_summary/chart/<company_id>')
# api.add_resource(CompanyFinancialPerformanceChart, '/api/company_financial/chart/<company_id>/<start_date>/<end_date>')
# api.add_resource(CompanySupplier, '/api/company_supplier/<data_provider_id>/<company_id>')
# api.add_resource(CompanySupplierChart, '/api/company_supplier/chart/<data_provider_id>/<company_id>/<max_level>')
# api.add_resource(CompanyESGFactorsChart, '/api/company_esg_factors/chart/<data_provider_id>/<company_id>', endpoint='esg_factors')
# api.add_resource(CompanyESGFactorsChart, '/api/company_esg_factors/chart/<data_provider_id>/<company_id>/<date_key>', endpoint='esg_factors_by_date')
# api.add_resource(CompanyAssetsChart, '/api/company_assets/chart/<company_id>')
# api.add_resource(CompanyESGSeries, '/api/company_esg_series/<data_provider_id>/<company_id>')



