#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import uimodules
import torndb

import settings
from operations.routes import route

define("debug", default=True, help="run in debug mode", type=bool)
define("port", default=8082, help="run on the given port", type=int)
define("showurls", default=False, help="Show all routed URLs", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = route.get_routes()
        server_settings = dict(
            title=settings.TITLE,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules=uimodules,
            cookie_secret=settings.COOKIE_SECRET,
            xsrf_cookies=True,
            login_url=settings.LOGIN_URL,
            debug=options.debug,
            webmaster=settings.WEBMASTER,
            admin_emails=settings.ADMIN_EMAILS,
        )
        self.mysql_db = torndb.Connection(settings.MYSQL_HOST,
                                          settings.MYSQL_DATABASE_NAME,
                                          settings.MYSQL_USER_NAME,
                                          settings.MYSQL_PASS_WORD)
        tornado.web.Application.__init__(self, handlers, **server_settings)


def main():
    tornado.options.parse_command_line()
    if options.showurls:
        for each in route.get_routes():
            print each._path.ljust(60),
            print each.handler_class.__name__
        return

    app = Application()
    app.listen(options.port)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass


def init():
    for handler_name in settings.HANDLERS:
        __import__('handlers.%s' % handler_name, globals(), locals(), [], -1)


if __name__ == '__main__':
    init()
    main()
