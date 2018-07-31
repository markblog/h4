from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from datetime import datetime
from esg.models.company_model import CompanyModel
from esg.models.company_primary_security_model import CompanyPrimarySecurityModel
from esg.models.company_esg_summary_model import CompanyEsgSummaryModel
from esg.models.company_supplier_model import CompanySupplierModel
from esg.models.security_model import SecurityModel
from esg.models.security_financial_series_model import SecurityFinancialSeriesModel
from operator import itemgetter
from ext import db


parser = reqparse.RequestParser()
parser.add_argument('company_id')
parser.add_argument('date')
parser.add_argument('closing_price')
parser.add_argument('volume')


class CompanyFinancialPerformanceChart(Resource):
    def get(self, company_id, start_date, end_date):
        final = self.get_performance_chart_by_dates(company_id, start_date, end_date)

        return jsonify(final)

    def get_performance_chart(self, company_id):
        models = SecurityFinancialSeriesModel.query.join(SecurityFinancialSeriesModel.security) \
            .join(CompanyPrimarySecurityModel, SecurityModel.company_id == CompanyPrimarySecurityModel.company_id) \
            .filter(CompanyPrimarySecurityModel.company_id == company_id, CompanyPrimarySecurityModel.asset_type_id == 1)\

        filtered = [self._get_perf(model) for model in models]

        final = self._format_models(filtered)

        return final

    def get_performance_chart_by_dates(self, company_id, start_date, end_date):
        models = SecurityFinancialSeriesModel.query.join(SecurityFinancialSeriesModel.security) \
            .join(CompanyPrimarySecurityModel, SecurityModel.company_id == CompanyPrimarySecurityModel.company_id) \
            .filter(
                CompanyPrimarySecurityModel.company_id == company_id, 
                CompanyPrimarySecurityModel.asset_type_id == 1,
                SecurityFinancialSeriesModel.date_key >= start_date,
                SecurityFinancialSeriesModel.date_key <= end_date)

        filtered = [self._get_perf(model) for model in models]

        final = self._format_models(filtered)

        return final

    def _format_models(self, models):
        return {
            'dimensions': ['Date', 'Closing Price', 'Volume'],
            'data': sorted(models, key = itemgetter(0), reverse = True)
        }

    def _get_perf(self, model):
        return [datetime.combine(model.date_key, datetime.min.time()).timestamp() * 1000, model.closing_price, model.volume if model.volume else 0]


class CompanySupplier(Resource):
    def get(self, data_provider_id, company_id):
        esg_info = db.session.query(CompanyEsgSummaryModel, CompanySupplierModel).\
            filter(
                CompanySupplierModel.company_id == company_id, 
                CompanyEsgSummaryModel.company_id == CompanySupplierModel.supplier_id, 
                CompanyEsgSummaryModel.data_provider_id == data_provider_id).\
            order_by(CompanyEsgSummaryModel.revenue).\
            all()

        result = [{
                'id': esg.CompanySupplierModel.supplier.id,
                'name': esg.CompanySupplierModel.supplier.name,
                'esg_score': esg.CompanyEsgSummaryModel.esg_score,
                'revenue': esg.CompanyEsgSummaryModel.revenue,
            } for esg in esg_info]

        return jsonify(result)


class CompanySupplierChart(Resource):
    def get(self, data_provider_id, company_id, max_level):
        result = self._get_level_info(data_provider_id, company_id, 1, int(max_level))

        return jsonify(result)

    def _get_level_info(self, data_provider_id, company_id, level, max_level):
        if level > max_level:
            return [];

        esg_info = db.session.query(CompanyEsgSummaryModel, CompanySupplierModel).\
            filter(
                CompanySupplierModel.company_id == company_id, 
                CompanyEsgSummaryModel.company_id == CompanySupplierModel.supplier_id, 
                CompanyEsgSummaryModel.data_provider_id == data_provider_id).\
            order_by(CompanyEsgSummaryModel.revenue).\
            all()

        result = []

        for esg in esg_info:
            supplier = esg.CompanySupplierModel.supplier

            result.append({
                'name': supplier.name,
                'esgScore': esg.CompanyEsgSummaryModel.esg_score,
                'revenue': esg.CompanyEsgSummaryModel.revenue,
                'children': self._get_level_info(data_provider_id, supplier.id, level + 1, max_level)
                })

        return result
