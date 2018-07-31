import logging
from flask import Flask, request
from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand
from logging.handlers import RotatingFileHandler
from flask_restful import Api
from ext import db
from manager import app

#init app 
app.config.from_object('config')
api = Api(app)
db.init_app(app)

#logging setting
formatter = logging.Formatter(app.config['LOG_FORMATTER'])
handler = RotatingFileHandler(app.config['SLOW_QUERY_LOG'], maxBytes=app.config['MAX_BYTES'], backupCount=app.config['BACKUP_COUNT'])
handler.setLevel(logging.WARN)
handler.setFormatter(formatter)
app.logger.addHandler(handler)


#add command for app
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)
manager.add_command('runserver',
					Server(use_debugger = True,use_reloader = True,host = app.config['HOST'],port=app.config['PORT'])
					)

@manager.command
def dropdb():
    db.drop_all()

@manager.command
def initdb():
    db.create_all()


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


#import blueprint here
import blueprint_register


