from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from manager import app
import application

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(9001)
IOLoop.instance().start()