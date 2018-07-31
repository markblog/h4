import application

from flask import Flask, jsonify, request
from flask_sqlalchemy import get_debug_queries
from flask import g
from flask_cors import CORS

from esg.request_errors import BadRequest

IMPORT_FOLDER = './uploads/import'

app = Flask(__name__)
app.config['IMPORT_FOLDER'] = IMPORT_FOLDER

CORS(app)


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# @app.before_request
# def before_request():
#     if 'session_id' not in request.cookies and 'logon' not in request.path:
#         return jsonify({'login_status':False})
#     else:
#         pass

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warn(
                ('\nSLOW QUERY:\n{}\n\nParameters:{}\nDuration:{}\n').format(query.statement, query.parameters,
                                                                             query.duration)
            )
    return response


if __name__ == '__main__':
    application.manager.run()
