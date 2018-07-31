#Server Setting
HOST = '127.0.0.1'
PORT = '9001'
DEBUG = True

#Database Settings
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:gxtagging@localhost/esg'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_QUERY_TIMEOUT = 10
SQLALCHEMY_RECORD_QUERIES = True
SQLALCHEMY_ECHO = False

#Log Path
LOG_FORMATTER = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
SLOW_QUERY_LOG = 'log/slow_query.log'
MAX_BYTES = 10000
BACKUP_COUNT = 10

#Data path
PORTFOLIOS_PATH = 'data/portfolios'
IMPORT_FOLDER = './uploads/import'

