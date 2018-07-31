from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#add your model here
from esg.models import esg_model, data_provider_model, geography_model, sector_model, correlation_group_model, \
    company_model, security_financial_series_model, company_primary_security_model,  \
    esg_rating_model, esg_factor_model, company_esg_factor_model, company_supplier_model, \
    company_esg_summary_model, asset_type_model, company_asset_model, portfolio_model, portfolio_result_model, \
    tag_category_model, tag_type_model, fixed_tag_model, esg_charts_model, weight_method_model, grouping_model,\
    metric_model, portfolio_grouping_metric_model

mc = {} # now I am using the dict replace the mc 
