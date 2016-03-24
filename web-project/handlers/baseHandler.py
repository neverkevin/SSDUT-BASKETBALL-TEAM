# -*- coding: utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    @property
    def mysql_db(self):
        return self.application.db

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        return username and username or None
