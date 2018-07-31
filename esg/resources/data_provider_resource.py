from flask import jsonify
from flask_restful import Resource

from esg.models.data_provider_model import DataProviderModel

class DataProviderList(Resource):
    def get(self):
        models = DataProviderModel.query.all()

        return jsonify([{'id': model.id, 'name': model.name} for model in models])


