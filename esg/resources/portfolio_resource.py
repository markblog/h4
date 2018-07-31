from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from esg.models.portfolio_model import PortfolioModel
from esg.resources.auth_resource import get_session_info
from ext import db

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('as_of')


class PortfolioModelList(Resource):
    def get(self):
        query = PortfolioModel.query

        organization_id, is_master_org, login_id = get_session_info(request)

        if not is_master_org:
            query = query.filter((PortfolioModel.owner_id == organization_id) | (PortfolioModel.owner_id == None))

        result = [model.serialize for model in query]
        return jsonify(result)

    def post(self):
        args = parser.parse_args()
        portfolio = PortfolioModel()
        portfolio.name = args["name"]
        portfolio.as_of = args["as_of"]
        db.session.add(portfolio)
        db.session.commit()
        return "OK", 201


class PortfolioSingleModel(Resource):
    def get(self, id):
        trl = PortfolioModel.query.filter_by(id=id).first()
        return jsonify({'result': trl.serialize()})


class PortfolioTags(Resource):
    def get(self):
        tags = []
        #tags.append({ 'id': 0, 'name': '< All Portfolios >'})

        models = PortfolioModel.query.all()

        for model in models:
            tags.append({ 'id': model.id, 'name': model.name})

        result = {
            'tag_type': 1,
            'values': tags
        }

        return jsonify(result)
