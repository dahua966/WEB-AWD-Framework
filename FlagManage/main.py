import threading
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from util import *

TEST = False

from tornado.options import define, options
define("port", default=6666, help="run on the given port", type=int)
define('address', default='0.0.0.0', help='binding at given address', type=str)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("please curl/wget myip/flag/(real flag)\n example: curl '127.0.0.1:6666/flag/flag{xxxxxx}'")

class PostFlagHandler(tornado.web.RequestHandler):
    def get(self,data):
        data = data.strip()
        if TEST:
            print '[+]Data: '+data
        else:
            res = postflag(data)
            self.write(res)

def main():
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/flag/(.*)', PostFlagHandler)],
        debug=False
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port,options.address)
    t = threading.Thread(target=tornado.ioloop.IOLoop.instance().start)
    t.daemon = True
    t.start()
    cmd_server()
    
if __name__ == '__main__':
    main()