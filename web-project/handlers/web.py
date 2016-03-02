# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import tornado
from urllib import quote
from urllib import unquote
from tornado import gen
from baseHandler import BaseHandler
from operations.routes import route
from models.model import *
from models import music


@route(r'/$', name='index')
class MainHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        if not self.get_secure_cookie("user"):
            self.render('index.html', url=url, username="登录")
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render('index.html', url=url, username=username)


@route(r'/test$', name='test')
class TestHandler(BaseHandler):
    def get(self):
        self.render('detail.html')


@route(r'/HallofFame$', name='mingrentang')
class HallofFameHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        contacts, total_contacts = yield GetContacts(self.application.mysql_db)
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render(
            'HallofFame.html', contacts=contacts, url=url,
            username=username, total_contacts=total_contacts
        )


@route(r'/history/([0-9]+)$', name='history/([0-9]+)')
class HistoryHandler(BaseHandler):
    def get(self, history_id):
        url = self.request.uri
        if not self.get_secure_cookie("user"):
            self.render(
                'history.html', history_id=history_id,
                url=url, username="登录"
            )
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render(
            'history.html', history_id=history_id,
            url=url, username=username
        )


@route(r'/add_contacts$', name='add_contacts')
class AddContactsHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def post(self):
        name = self.get_argument('name')
        grade = self.get_argument('grade')
        phonenum = self.get_argument('phonenum')
        place = self.get_argument('place')
        yield AddContacts(
            self.application.mysql_db, name, grade, phonenum, place
        )
        self.redirect('/HallofFame', permanent=True)


@route(r'/user/\S+', name='user')
class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        username = tornado.escape.xhtml_escape(self.current_user)
        if url != '/user/{}'.format(quote(username)):
            raise tornado.web.HTTPError(403)
        self.render('user.html', url=url, username=username)


@route(r'/Music', name='Music')
class MusicHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        if url == '/Music':
            songs = music.query('mylove')
        else:
            songs = music.query(self.get_argument('song'))
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render('Music.html', username=username, url=url, songs=songs)


@route(r'/login$', name='login')
class LoginHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('login.html', url=url, username="登录", error=None)

    @gen.coroutine
    def post(self):
        data = self.request.body
        username = unquote(re.findall('username=([^&]*)', data)[0])
        password = unquote(re.findall('passowrd=([^&]*)', data)[0])
        result = yield login(self.application.mysql_db, username, password)
        if result == '1':
            nickname = yield get_nickname(self.application.mysql_db, username)
            self.set_secure_cookie("user", nickname)
        self.write(result)
        # if result is True:
        #     nickname = yield get_nickname(self.application.mysql_db, username)
        #     self.set_secure_cookie("user", nickname)
        #     self.redirect("/HallofFame", permanent=True)

        # else:
        #     url = self.request.uri
        #     self.render("login.html", url=url, username="登录", error=result)


@route(r'/logout$', name='logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/", permanent=True)


@route(r'/register$', name='register')
class RegisterHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        if not self.get_secure_cookie("user"):
            self.render('register.html', url=url, username="登录", error=None)
        username = tornado.escape.xhtml_escape(self.current_user)
        self.render(
            'register.html', url=url, username=username, error=None
        )

    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        nickname = self.get_argument('nickname')
        password = self.get_argument('password')
        secretcode = self.get_argument('Secretcode')
        result = yield register(
            self.application.mysql_db, username, nickname, password, secretcode
        )
        if result is True:
            self.redirect("/login", permanent=True)

        else:
            url = self.request.uri
            self.render("register.html", url=url, username="登录", error=result)
