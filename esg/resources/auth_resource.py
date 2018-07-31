from flask import request, jsonify, make_response, abort
from flask_restful import Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from esg.models.login_model import LoginModel
from esg.request_errors import BadRequest

from ext import db

def get_session_info(request):
    """Given the request object, retrieves the users organization id.
    """
    if 'session_id' not in request.cookies:
        session_id = None
    else:
        session_id = request.cookies['session_id']

    if session_id is not None:
        Session = sessionmaker(bind=db.engine)
        session = Session()

        query = text("select * from membership.validate_session(:id)")
        query_result = session.execute(query, { 'id': session_id }).first()

        if query_result is not None:
            session.commit()
            return query_result['organization_id'], query_result['is_master'], query_result['login_id']
    else:
        abort(401)
        #return 1, True, 1


class UserLogon(Resource):
    def post(self):
        """Given form values of login_name and password, logs the user in and creates a session.

        Upon successful completion, a cookie will be set with the session id.

        Returns:
            JSON containing success flag, login id, and session id.
        """
        success = False
        session_id = None
        login_id = None

        login_name = request.form['login_name']
        password = request.form['password']

        Session = sessionmaker(bind=db.engine)
        session = Session()

        sql = text("select * from membership.logon(:ln, :pwd)")
        query_result = session.execute(sql, {'ln': login_name, 'pwd': password}).first()

        if query_result is not None:
            success = query_result['success']
            login_id = query_result['login_id']
            session_id = query_result['session_id']

            session.commit()

        response = jsonify({ 'success': success, 'login_id': login_id, 'session_id': session_id })
        
        if success:
            response.set_cookie('session_id', session_id)
            
        return response


class UserLogoff(Resource):
    def post(self):
        """Logs off the user specified by the given session id.
        """
        if not 'session_id' in request.cookies:
            raise BadRequest('Could not find session_id cookie')

        session_id = request.cookies['session_id']

        Session = sessionmaker(bind=db.engine)
        session = Session()

        sql = text("select * from membership.logoff(:sid)")
        session.execute(sql, {'sid': session_id})
        session.commit()


class UserProfile(Resource):
    def get(self):
        profile = None

        _, _, login_id = get_session_info(request)

        if login_id is not None:
            login = LoginModel.query.get(login_id)

            profile = {
                'login_id': login.id,
                'login_name': login.login_name,
                'display_name': login.display_name,
                'email': login.email,
                'organization_name': login.organization.name
            }

        return jsonify(profile)
