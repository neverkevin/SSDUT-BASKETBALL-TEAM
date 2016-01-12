# -*- coding: utf-8 -*-

import tornado.web
import torndb


class BaseHandler(tornado.web.RequestHandler):
    @property
    def mysql_db(self):
        return self.application.mysql_db

    def get_current_user(self):
        '''
            auth user
        '''
        return self.get_secure_cookie("user")
        #username = self.get_secure_cookie("user")
        #if not username: return None
        #return self.mysql_db.get("SELECT username FROM user WHERE username = %s",
        #        username)

    def get_login_url(self):
        '''
            override login_url
        '''
        return "/login"
