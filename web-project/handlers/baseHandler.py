# -*- coding: utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        '''
            auth user
        '''
        return self.get_secure_cookie("name")

    def get_login_url(self):
        '''
            override login_url
        '''
        return "/login"
