import time
from flask import jsonify
from flask_restful import Resource
from sqlalchemy.sql import text

from esg.models.company_model import CompanyModel
from esg.models.company_asset_model import CompanyAssetModel
from esg.models.data_provider_model import DataProviderModel
from esg.models.esg_factor_model import EsgFactorModel
from esg.resources.company_financial_series_resource import CompanyFinancialPerformanceChart
from esg.resources.esg_resource import CompanyESGFactorsChart
from ext import db


class CompanyList(Resource):
    def get(self):
        models = CompanyModel.query.all()

        #return jsonify([model.serialize for model in models])
        return jsonify([{'id': model.id, 'name': model.name} for model in models])


class CompanyAsset(Resource):
    def get(self, company_id):
        models = CompanyAssetModel.query.filter(
            CompanyAssetModel.company_id == company_id)

        return jsonify([model.serialize for model in models])


class CompanyAssetsChart(Resource):
    ID = 0
    NAME = 1
    LEVEL = 2
    PARENT = 3
    VOLUME = 4
    GRP_PERCENT = 5

    def get(self, company_id):
        infos = db.engine.execute("""
select a.id, a.name, a.level, a.parent_id, c.volume,
  case when pg.total_by_parent = 0 then 0 else abs(volume) / pg.total_by_parent end as group_percentage
from company_asset c join asset_type a on c.asset_type_id = a.id
  left outer join (
    select a.parent_id, sum(abs(c.volume)) as total_by_parent
    from company_asset c join asset_type a on c.asset_type_id = a.id
    group by a.parent_id
  ) pg on a.parent_id = pg.parent_id or (a.parent_id IS NULL AND pg.parent_id IS NULL)
where c.company_id = '""" + company_id + """'
order by a.level, a.id""")

        result = []

        # Read into a list we can iterate over multiple times
        models = [info for info in infos]

        for model in models:
            if model[self.LEVEL] == 1:
                info = self._get_asset_info(model, models, 1)
                result.append(info)

        return jsonify(result)

    def _get_asset_info(self, model, all_models, parent_weight):
        group_percent = model[self.GRP_PERCENT]
        asset_percent = group_percent * parent_weight

        return {
            'id': model[self.ID],
            'name': model[self.NAME],
            'level': model[self.LEVEL],
            'volume': model[self.VOLUME],
            'percentage': asset_percent,
            'children': self._get_child_models(all_models, model[self.ID], asset_percent)
        }

    def _get_child_models(self, all_models, parent_id, parent_weight):
        children = []

        for model in all_models:
            if (parent_id is None and model[self.LEVEL] == 1) or model[self.PARENT] == parent_id:
                children.append(self._get_asset_info(model, all_models, parent_weight))

        return children


class CompanyESGSeries(Resource):
    def get(self, data_provider_id, company_id):
        series = self.get_esg_series_data(data_provider_id, company_id)

        return jsonify(series)

    @staticmethod
    def get_esg_series_data(data_provider_id, company_id):
        factors_query = EsgFactorModel.query \
            .filter(EsgFactorModel.data_provider_id == data_provider_id, EsgFactorModel.level <= 2) \
            .order_by(EsgFactorModel.level, EsgFactorModel.id)

        dimensions = [metric.name for metric in factors_query]
        dimensions.insert(0, "Date")

        #esg_series_query = CompanyEsgFactorModel.query.join(CompanyEsgFactorModel.esg_factor) \
        #    .filter(EsgFactorModel.data_provider_id == data_provider_id, CompanyEsgFactorModel.company_id == company_id, EsgFactorModel.level <= 2) \
        #    .order_by(CompanyEsgFactorModel.date_key, EsgFactorModel.level, EsgFactorModel.id)

        query_text = text("select * from get_esg_summary_series(:cid, :dpid)")
        esg_series_query = db.engine.execute(query_text, cid = company_id, dpid = data_provider_id)

        esg_series = []

        current_date = None
        esg_series_date = None

        for esg_values in esg_series_query:
            if current_date != esg_values.date_key:
                if esg_series_date is not None:
                    esg_series.append(esg_series_date)

                current_date = esg_values.date_key
                esg_series_date = [time.mktime(current_date.timetuple()) * 1000]

            esg_series_date.append(esg_values.score)

        if esg_series_date is not None:
            esg_series.append(esg_series_date)

        return {'dimensions': dimensions, 'data': esg_series}

    @staticmethod
    def _get_esg_series(model):
        return [time.mktime(model.date_key.timetuple()) * 1000, model.e_score, model.s_score, model.g_score]


class CompanyESGSummary(Resource):
    def get(self, data_provider_id = None, company_id = None):
        if data_provider_id is None:
            data_provider = DataProviderModel.query.order_by(DataProviderModel.name).first()

            if data_provider is not None:
                data_provider_id = data_provider.id

        if company_id is None:
            company = CompanyModel.query.order_by(CompanyModel.name).first()

            if company is not None:
                company_id = company.id

        if data_provider_id is not None and company_id is not None:
            result = self.get_company_esg_summary(data_provider_id, company_id)

            return result
        else:
            return {}

    def get_company_esg_summary(self, data_provider_id, company_id):
        data_provider = DataProviderModel.query.get(data_provider_id)
        company = CompanyModel.query.get(company_id)
        esg_factors = CompanyESGFactorsChart().get_company_esg_factors(data_provider_id, company_id)
        esg_scores = CompanyESGSeries.get_esg_series_data(data_provider_id, company_id)
        financial_performance = CompanyFinancialPerformanceChart().get_performance_chart(company_id)

        result = { 
            'data_provider_id': data_provider_id,
            'company_id': company_id,
            'data_provider_name': data_provider.name if data_provider is not None else '',
            'company_name': company.name if company is not None else '',
            'factors': esg_factors,
            'score': esg_scores,
            'financial_performance': financial_performance
            }

        return jsonify(result)
