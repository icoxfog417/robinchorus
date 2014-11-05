import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
from handlers import GroupHandler, ChatHandler, ChatsHandler, ChatSocketHandler, StampHandler


class Application(tornado.web.Application):
    """
    Please define os environment variable
    * SECRET_TOKEN: secret key for storing secure cookie
    * PORT: port number
    """

    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/group", GroupHandler),
            (r"/chat/([^/]+)", ChatHandler),
            (r"/chat/([^/]+)/socket", ChatSocketHandler),
            (r"/chat/([^/]+)/chats", ChatsHandler),
            (r"/chat/([^/]+)/stamps", StampHandler)
        ]
        settings = dict(
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class HomeHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


def main():
    app = Application()
    app.listen(int(os.environ.get("PORT", 8080)))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
