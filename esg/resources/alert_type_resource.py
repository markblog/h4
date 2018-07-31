from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from esg.models.alert_digest_history_model import AlertDigestHistoryModel
from esg.resources.auth_resource import get_session_info
from esg.resources.tag_type_resource import TagType
from ext import db


class AlertList(Resource):
    def get(self):
        organization_id, is_master_org, login_id = get_session_info(request)

        search_tags_query = db.engine.execute("select * from get_alert_search_tags()")
        all_search_tags = []
        for d in search_tags_query:
            all_search_tags.append(dict(d.items()))

        query_text = text("select * from get_alert_history(:lid)")
        alerts = []
        alert_history_id = None
        first_alert_info = None
        alert_values = []

        for alert_info in db.engine.execute(query_text, lid=login_id):
            if alert_info['alert_history_id'] != alert_history_id:
                self.add_alert(first_alert_info, alert_values, alerts, all_search_tags)

                alert_history_id = alert_info['alert_history_id']
                first_alert_info = dict(alert_info.items())
                alert_values = []

            alert_values.append(alert_info['value'])

        self.add_alert(first_alert_info, alert_values, alerts, all_search_tags)

        return jsonify(alerts)

    @staticmethod
    def add_alert(alert_info, alert_values, alerts, all_search_tags):
        if alert_info is not None:
            alert = {
                'alert_history_id': alert_info['alert_history_id'],
                'alert_text': alert_info['text_template'].format(*alert_values),
                'date_key': datetime.combine(alert_info['date_key'], datetime.min.time()).timestamp() * 1000,
                'is_new': alert_info['is_new']
            }

            if alert_info['target'] == 'p':
                alert['tags'] = AlertList.get_search_tags(alert_info, all_search_tags)
            else:
                alert['company_esg_info'] = {
                    'data_provider_id': alert_info['data_provider_id'],
                    'data_provider_name': alert_info['data_provider_name'],
                    'company_id': alert_info['company_id'],
                    'company_name': alert_info['company_name']
                }

            alerts.append(alert)

    @staticmethod
    def get_search_tags(alert_info, all_search_tags):
        search_tags = [t for t in all_search_tags if t['alert_history_id'] == alert_info['alert_history_id']]
        result = []

        for search_tag in search_tags:
            tag = { 'tag_type_id': search_tag['tag_type_id'] }
            if search_tag['tag_name'] is None:
                if search_tag['tag_type_id'] == TagType.PORTFOLIO:
                    tag['id'] = search_tag['portfolio_id']
                    tag['name'] = search_tag['portfolio_name']
                elif search_tag['tag_type_id'] == TagType.ESG_METRICS:
                    tag['id'] = search_tag['esg_factor_id']
                    tag['name'] = search_tag['esg_factor_name']
                elif search_tag['tag_type_id'] == TagType.REGION:
                    if search_tag['region_id'] is not None:
                        tag['id'] = search_tag['region_id']
                        tag['name'] = search_tag['region_name']
                    elif search_tag['country_id'] is not None:
                        tag['id'] = search_tag['country_id']
                        tag['name'] = search_tag['country_name']
                    tag['level'] = search_tag['level']
                elif search_tag['tag_type_id'] == TagType.SECTOR:
                    if search_tag['sector_id'] is not None:
                        tag['id'] = search_tag['sector_id']
                        tag['name'] = search_tag['sector_name']
                    elif search_tag['industry_id'] is not None:
                        tag['id'] = search_tag['industry_id']
                        tag['name'] = search_tag['industry_name']
                    tag['level'] = search_tag['level']
                elif search_tag['tag_type_id'] == TagType.TIME:
                    tag['id'] = search_tag['tag_id']
                    tag['name'] = search_tag['tag_name']
                elif search_tag['tag_type_id'] == TagType.DATE:
                    tag['id'] = search_tag['tag_id']
                    tag['name'] = str(search_tag['date_key'])
            else:
                tag['id'] = search_tag['tag_id']
                tag['name'] = search_tag['tag_name']

            result.append(tag)

        return result


class AlertMarkRead(Resource):
    def post(self, alert_history_id):
        """Given an alert_id, marks it read by the currently logged in user
        
        Returns:
            JSON containing success flag.
        """
        status = 'SUCCESS'

        try:
            _, _, login_id = get_session_info(request)

            Session = sessionmaker(bind=db.engine)
            session = Session()

            query = text("select * from alert_mark_read(:hid, :lid)")
            session.execute(query, {'hid': int(alert_history_id), 'lid': login_id})

            session.commit()

        except Exception as e:
            status = 'FAILED'

        return jsonify({'status': status})


class AlertMarkAllRead(Resource):
    def post(self):
        """Marks all existing alerts as read by the currently logged in user

        Returns:
            JSON containing success flag.
        """
        status = 'SUCCESS'

        try:
            _, _, login_id = get_session_info(request)

            Session = sessionmaker(bind=db.engine)
            session = Session()

            query = text("select * from alert_mark_all_read(:lid)")
            session.execute(query, {'lid': login_id})

            session.commit()

        except Exception as e:
            status = 'FAILED'

        return jsonify({'status': status})


class AlertDismiss(Resource):
    def post(self, alert_history_id):
        """Given an alert_id, marks it read by the currently logged in user

        Returns:
            JSON containing success flag.
        """
        status = 'SUCCESS'

        try:
            _, _, login_id = get_session_info(request)

            Session = sessionmaker(bind=db.engine)
            session = Session()

            query = text("select * from alert_dismiss(:hid, :lid)")
            session.execute(query, {'hid': int(alert_history_id), 'lid': login_id})

            session.commit()

        except Exception as e:
            status = 'FAILED'

        return jsonify({'status': status})


class AlertDismissAll(Resource):
    def post(self):
        """Dismisses all existing alerts available to the currently logged in user

        Returns:
            JSON containing success flag.
        """
        status = 'SUCCESS'

        try:
            _, _, login_id = get_session_info(request)

            Session = sessionmaker(bind=db.engine)
            session = Session()

            query = text("select * from alert_dismiss_all(:lid)")
            session.execute(query, {'lid': login_id})

            session.commit()

        except Exception as e:
            status = 'FAILED'

        return jsonify({'status': status})


