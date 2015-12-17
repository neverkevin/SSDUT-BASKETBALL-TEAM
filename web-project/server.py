#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import uimodules

import settings
import torndb
from operations.routes import route
from mongoengine.connection import connect

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=2358, help="run on the given port", type=int)
define("showurls", default=False, help="Show all routed URLs", type=bool)
define("database_name", default=settings.DEFAULT_DATABASE_NAME, help="database name")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = route.get_routes()
        server_settings = dict(
            title=settings.TITLE,
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules=uimodules,
            cookie_secret=settings.COOKIE_SECRET,
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

    connect(options.database_name)


if __name__ == '__main__':
    init()
    main()
