import os

from flask import request, jsonify, send_from_directory
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from ext import db
from config import PORTFOLIOS_PATH


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')


class PortfolioDataManager(Resource):

    def post(self):
        args = parser.parse_args()
        file = args["file"]
        if file:
            file_name = file.filename
            print(file_name)
            file.save(os.path.join(PORTFOLIOS_PATH,file_name))
        return "OK", 201

    def get(self,file_name):
        return send_from_directory(PORTFOLIOS_PATH, file_name)
