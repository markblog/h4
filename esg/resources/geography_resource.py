from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from esg.models.geography_model import GeographyModel
from ext import db

parser = reqparse.RequestParser()
parser.add_argument('name')


class GeographyModelList(Resource):
    def get(self):
        trls = GeographyModel.query.all()
        return jsonify({'result': [trl.serialize() for trl in trls]})

    def post(self):
        args = parser.parse_args()
        geography = GeographyModel()
        geography.geography_name = args["name"]
        db.session.add(geography)
        db.session.commit()
        return "OK", 201


class GeographySingleModel(Resource):
    def get(self, id):
        trl = GeographyModel.query.filter_by(id=id).first()
        return jsonify({'result': trl.serialize()})
