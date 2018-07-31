from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from sqlalchemy.sql import text
from esg.models.esg_model import ESGSimpleDemoModel
from esg.models.company_esg_summary_model import CompanyEsgSummaryModel
from ext import db

parser = reqparse.RequestParser()
parser.add_argument('name')


class ESGSimpleDemoModelList(Resource):
    def get(self):
        trls = ESGSimpleDemoModel.query.all()
        return jsonify({'result': [trl.serialize() for trl in trls]})

    def post(self):
        args = parser.parse_args()
        esg = ESGSimpleDemoModel()
        esg.company_name = args["name"]
        db.session.add(esg)
        db.session.commit()
        return "OK", 201


class ESGSummary(Resource):
    def get(self, company_id):
        esg = CompanyEsgSummaryModel.query.filter(CompanyEsgSummaryModel.company_id == company_id).all()
        return jsonify([model.serialize for model in esg])


class ESGSummaryChart(Resource):
    def get(self, company_id):
        esg = CompanyEsgSummaryModel.query.filter(CompanyEsgSummaryModel.company_id == company_id).all()

        categories = []
        ratings = []
        es = []
        ss = []
        gs = []

        for model in esg:
            categories.append(model.data_provider_id)
            ratings.append(model.rating_id)
            es.append(model.e_score)
            ss.append(model.s_score)
            gs.append(model.g_score)

        final = {
            'categories': categories,
            'esgdata': [{
                'name': 'Rating',
                'data': ratings
            },
                {
                    'name': 'E',
                    'data': es
                },
                {
                    'name': 'S',
                    'data': ss
                },
                {
                    'name': 'G',
                    'data': gs
                }
            ]
        }

        return jsonify(final)

    def _get_esg(self, model):
        return [model.date.timestamp(), model.closing_price, model.volume]


class CompanyESGFactorsChart(Resource):
    ID = 0
    NAME = 1
    ESG_TYPE = 2
    LEVEL = 3
    PARENT = 4
    SCORE = 5
    UNWEIGHTED_PERCENT = 6
    WEIGHTED_SCORE = 7
    WEIGHTED_PERCENT = 8

    def get(self, data_provider_id, company_id, date_key = None):
        company_esg_factors = self.get_company_esg_factors(data_provider_id, company_id, date_key)

        return jsonify(company_esg_factors)

    def get_company_esg_factors(self, data_provider_id, company_id, date_key = None):
        if date_key is None:
            query_text = text("select * from get_company_esg_factor_percentages(:cid, :dpid)")
            model_query = db.engine.execute(query_text, cid = company_id, dpid = data_provider_id)
        else:
            query_text = text("select * from get_company_esg_factor_percentages(:cid, :dpid, :dk)")
            model_query = db.engine.execute(query_text, cid = company_id, dpid = data_provider_id, dk = date_key)

        return self._get_factors_from_query(model_query)

    def _get_factors_from_query(self, model_query):
        # Read into a list we can iterate over multiple times
        models = [info for info in model_query]
        result = None

        for model in models:
            if model[self.LEVEL] == 1:
                info = self._get_factor_info(model, models)
                result = info

        return result

    def _get_factor_info(self, model, all_models):
        return {
            'id': model[self.ID],
            'name': model[self.NAME],
            'esg_type': model[self.ESG_TYPE],
            'level': model[self.LEVEL],
            'score': model[self.SCORE],
            'percentage': model[self.UNWEIGHTED_PERCENT],
            'weighted_score': model[self.WEIGHTED_SCORE],
            'weighted_percentage': model[self.WEIGHTED_PERCENT],
            'children': self._get_child_models(all_models, model[self.ID])
        }

    def _get_child_models(self, all_models, parent_id):
        children = []

        for model in all_models:
            if (parent_id is None and model[self.LEVEL] == 1) or model[self.PARENT] == parent_id:
                children.append(self._get_factor_info(model, all_models))

        return children
