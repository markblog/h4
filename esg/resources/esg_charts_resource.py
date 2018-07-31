import datetime
import traceback

from flask import request, jsonify
from flask_restful import Resource

from esg.request_errors import BadRequest
from esg.services.charts.charts_factory import ChartFactory
from esg.services.charts.charting_rules import TagTypeChart, ChartingRules


class EsgChartsRouting(Resource):
    
    def post(self):
        result = []
        chart = None
        json = request.get_json()
        if json is None:
            raise BadRequest('JSON POST was expected')

        charting_rules = ChartingRules(json)

        try:

            chart_factory = ChartFactory(charting_rules)
            chart = chart_factory.get_chart_instance_with_refection()
            
            if chart:
                chart.fetch_data(parameters_dic = charting_rules.dic)

                if not self._is_empty(chart.data):
                    result = {'status': 'SUCCESS', 'code': 200, 'data': chart.as_dict()}
                else:
                    result = {'status': 'FAILED', 'code': 404, 'data': 'No data available for this combination'}

            else:
                result = {'message': charting_rules.error_message, 'status': 'FAILED', 'code': 404}
                
        except Exception as e:
            traceback.print_exc()
            result = {'message': e.message, 'status':'FAILED', 'code': 401}

        return jsonify(result)

    @staticmethod
    def _get_tags_by_type(json, tag_type):
        return [tag for tag in json if tag['tag_type_id'] == tag_type]

    def _is_empty(self, parameters_list):
        return parameters_list is None or len(parameters_list) == 0
