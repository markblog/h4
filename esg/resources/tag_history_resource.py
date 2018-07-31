from flask import jsonify, request, json
from flask_restful import Resource, reqparse

from esg.models.tag_history_model import TagHistoryModel
from esg.request_errors import BadRequest
from ext import db
from esg.resources.auth_resource import get_session_info

parser = reqparse.RequestParser()
parser.add_argument('delete')
parser.add_argument('id')

class TagHistory(Resource):
    init_flag = 0

    def post(self):
        _,_,owner_id=get_session_info(request)
        json = request.get_json()
        if json is None:
            raise BadRequest('JSON POST was expected')
        try:
            tag_history = TagHistoryModel()
            tag_history.owner_id = owner_id
            if not json['name']:
                return jsonify({'success': 0, 'message':'Please enter a name.'})
            if not json['tag_combination']:
                return jsonify({'success': 0 , 'message':' You can’t leave this search bar empty.'})
            if json['name'] and json['tag_combination']:
                models = TagHistoryModel.query.filter(TagHistoryModel.owner_id == owner_id,\
                                                        TagHistoryModel.name == json['name']).all()
                if not models:
                    tag_history.name = json['name']
                    tag_history.tag_combination = json['tag_combination']
                    db.session.add(tag_history)
                    db.session.commit()
                    return jsonify({'success': 1})
                else:
                    return jsonify({'success': 0, 'message':'Name is taken. Try again.'})
        except:
            db.session.rollback()
            jsonify({'success': 0})
        finally:
            db.session.close()


    def get(self):
        _,_,owner_id=get_session_info(request)
        TagHistory.init_flag = 0
        if TagHistory.init_flag == 1:
            self.init_defalut_value()
            TagHistory.init_flag = 0
        args = parser.parse_args()
        if args['delete']:
            TagHistoryModel.query.delete()
            db.session.commit()
            return 'ok', 201
        models = TagHistoryModel.query.filter(TagHistoryModel.owner_id == owner_id).order_by(TagHistoryModel.id.desc()).all()
        result = [model.serialize for model in models]
        return jsonify(result)

    def delete(self):
        args = parser.parse_args()
        delete_id = args['id']
        TagHistoryModel.query.filter(TagHistoryModel.id == delete_id).delete()
        db.session.commit()

    def init_defalut_value(self):
        init_values01 = []
        init_values02 = []
        init_values03 = []
        init_values04 = []
        init_values05 = []
        init_values06 = []
        init_values07 = []
        init_values08 = []
        init_values09 = []
        init_values10 = []

        tag_title_chart1 = 'ESG Distribution Histogram'
        init_values01.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values01.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values01.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})

        tag_title_chart2 = 'Multiple Channel ESG Score Distribution Histogram'
        init_values02.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values02.append({"id": 7, "name": "Arabesque ESG Environment Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values02.append({"id": 8, "name": "Arabesque ESG Social Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values02.append({"id": 9, "name": "Arabesque ESG Governance Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})

        tag_title_chart3 = 'ESG Distribution by Industry'
        init_values03.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values03.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values03.append({"id": 10, "level": 1, "name": "Energy", "tag_type_id": 5})
        init_values03.append({"id": 40, "level": 1, "name": "Financials", "tag_type_id": 5})
        init_values03.append({"id": 35, "level": 1, "name": "Health Care", "tag_type_id": 5})
        init_values03.append({"id": 5, "name": "All Industries", "tag_type_id": 7})
        init_values03.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values03.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})

        tag_title_chart4 = 'UNGC Score details'
        init_values04.append({"id": 1001, "name": "Portfolio A", "tag_type_id": 1})
        init_values04.append({"id": 21, "name": "Arabesque UNGC Details", "tag_type_id": 7})
        init_values04.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})


        tag_title_chart5 = 'ESG Distribution by Geography'
        init_values05.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values05.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values05.append({"id": 10, "level": 1, "name": "Asia Pacific Developed", "tag_type_id": 4})
        init_values05.append({"id": 20, "level": 1, "name": "Asia Pacific Emerging", "tag_type_id": 4})
        init_values05.append({"id": 30, "level": 1, "name": "Europe Developed", "tag_type_id": 4})
        init_values05.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values05.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})

        tag_title_chart6 = 'ESG Time series'
        init_values06.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values06.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values06.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values06.append({"id": 5, "name": "Time (Daily)", "tag_type_id": 6})
        init_values06.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})

        tag_title_chart7 = 'Multiple channel ESG Score Time Series'
        init_values07.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values07.append({"id": 7, "name": "Arabesque ESG Environment Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values07.append({"id": 8, "name": "Arabesque ESG Social Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values07.append({"id": 9, "name": "Arabesque ESG Governance Score", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values07.append({"id": 5, "name": "Time (Daily)", "tag_type_id": 6})
        init_values07.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})
        

        tag_title_chart8 = 'Performance by ESG Time Series'
        init_values08.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values08.append({"id": 1, "name": "Analysis", "tag_type_id": 9})
        init_values08.append({"id": 4, "name": "Cumulative Return", "tag_type_id": 3})
        init_values08.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values08.append({"id": 5, "name": "Time (Daily)", "tag_type_id": 6})

        tag_title_chart9 = 'ESG Score by weight'
        init_values09.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values09.append({"id": 1, "name": "All Securities", "tag_type_id": 7})
        init_values09.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})


        tag_title_chart10 = 'ESG Distribution Filtered by Region and Industry'
        init_values10.append({"id": 1003, "name": "allan_12_stock_test_portfolio", "tag_type_id": 1})
        init_values10.append({"id": 1004, "name": "GX1000", "tag_type_id": 1})
        init_values10.append({"id": 10, "level": 1, "name": "Energy", "tag_type_id": 5})
        init_values10.append({"id": 2, "level": 1, "name": "All Regions", "tag_type_id": 7})
        init_values10.append({"id": 6, "name": "Arabesque ESG", "provider_name": "Arabesque ESG", "tag_type_id": 2})
        init_values10.append({"id": 1, "name": "Weight by value", "tag_type_id": 8})


        tag_history_01 = TagHistoryModel()
        tag_history_02 = TagHistoryModel()
        tag_history_03 = TagHistoryModel()
        tag_history_04 = TagHistoryModel()
        tag_history_05 = TagHistoryModel()
        tag_history_06 = TagHistoryModel()
        tag_history_07 = TagHistoryModel()
        tag_history_08 = TagHistoryModel()
        tag_history_09 = TagHistoryModel()
        tag_history_10 = TagHistoryModel()

        tag_history_01.name = tag_title_chart1
        tag_history_01.tag_combination = init_values01
        tag_history_02.name = tag_title_chart2
        tag_history_02.tag_combination = init_values02
        tag_history_03.name = tag_title_chart3
        tag_history_03.tag_combination = init_values03
        tag_history_04.name = tag_title_chart4
        tag_history_04.tag_combination = init_values04
        tag_history_05.name = tag_title_chart5
        tag_history_05.tag_combination = init_values05
        tag_history_06.name = tag_title_chart6
        tag_history_06.tag_combination = init_values06
        tag_history_07.name = tag_title_chart7
        tag_history_07.tag_combination = init_values07
        tag_history_08.name = tag_title_chart8
        tag_history_08.tag_combination = init_values08
        tag_history_09.name = tag_title_chart9
        tag_history_09.tag_combination = init_values09
        tag_history_10.name = tag_title_chart10
        tag_history_10.tag_combination = init_values10

        TagHistoryModel.query.delete()
        db.session.commit()


        db.session.add(tag_history_01)
        db.session.add(tag_history_02)
        db.session.add(tag_history_03)
        db.session.add(tag_history_04)
        db.session.add(tag_history_05)
        db.session.add(tag_history_06)
        db.session.add(tag_history_07)
        db.session.add(tag_history_08)
        db.session.add(tag_history_09)
        db.session.add(tag_history_10)
        db.session.commit()


