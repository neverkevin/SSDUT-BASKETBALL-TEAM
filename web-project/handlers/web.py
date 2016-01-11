#/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
from baseHandler import BaseHandler
from operations.routes import route
from tornado import gen
from models.model import *


@gen.coroutine
@route(r'/$', name='index')
class MainHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        if self.get_secure_cookie("user"):
            username = tornado.escape.xhtml_escape(self.current_user)
            self.render('index.html', url=url, username=username)
        else:
            self.render('index.html', url=url, username="登录")


@route(r'/mingrentang$', name='mingrentang')
class MingrentangHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        contacts = GetContacts(self.application.mysql_db)
        if self.get_secure_cookie("user"):
            username = tornado.escape.xhtml_escape(self.current_user)
            self.render('mingrentang.html', contacts=contacts, url=url, username=username)
        else:
            self.render('mingrentang.html', contacts=contacts, url=url, username="登录")


@route(r'/history/([0-9]+)$', name='history/([0-9]+)')
class HistoryHandler(BaseHandler):
    def get(self, history_id):
        url = self.request.uri
        if self.get_secure_cookie("user"):
            username = tornado.escape.xhtml_escape(self.current_user)
            self.render('history.html', history_id=history_id, url=url, username=username)
        else:
            self.render('history.html', history_id=history_id, url=url, username="登录")


@route(r'/add_contacts$', name='add_contacts')
class AddContactsHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        grade = self.get_argument('grade')
        phonenum = self.get_argument('phonenum')
        place = self.get_argument('place')
        alert = AddContacts(self.application.mysql_db, name, grade, phonenum, place)
        self.redirect('/mingrentang', permanent=True)


@route(r'/login$', name='login')
class LoginHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('login.html', url=url, username="登录")

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        tag = login(self.application.mysql_db, username, password)
        if tag == True:
            nickname = get_nickname(self.application.mysql_db, username)
            self.set_secure_cookie("user", nickname)
            self.redirect("/mingrentang", permanent=True)
        else:
            self.redirect("/login", permanent=True)


@route(r'/logout$', name='logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/", permanent=True)


@route(r'/register$', name='register')
class RegisterHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        if self.get_secure_cookie("user"):
            username = tornado.escape.xhtml_escape(self.current_user)
            self.render('register.html', url=url, username=username)
        else:
            self.render('register.html', url=url, username='登录')

    def post(self):
        username = self.get_argument('username')
        nickname = self.get_argument('nickname')
        password = self.get_argument('password')
        secretcode = self.get_argument('Secretcode')
        result = register(self.application.mysql_db, username, nickname, password, secretcode)
        if result == True:
            self.redirect("/login", permanent=True)
        else:
            self.redirect("/register", permanent=True)
