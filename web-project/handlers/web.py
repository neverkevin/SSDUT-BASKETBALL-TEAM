# /usr/bin/env python
# -*- coding: utf-8 -*-

import re
import tornado
from urllib import quote
from urllib import unquote
from tornado import gen
from baseHandler import BaseHandler
from operations.routes import route
from models import model
from models import music


@route(r'/$', name='home')
class MainHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        if not self.get_secure_cookie("user"):
            self.render('index.html', url=url, username="登录")
        else:
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
        contacts, total_contacts = yield model.get_contacts(self.mysql_db)
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
        yield model.add_contacts(
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
        result = yield model.login(
            self.application.mysql_db, username, password
            )
        if result == '1':
            nickname = yield model.get_nickname(
                self.application.mysql_db, username
                )
            self.set_secure_cookie("user", nickname)
        self.write(result)


@route(r'/check_username', name='checkout_username')
class CheckUsernameHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        data = self.request.body
        username = unquote(re.findall('username=([^&]*)', data)[0])
        result = yield model.check_username(
            self.application.mysql_db, username
            )
        self.write(result)


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
        data = self.request.body
        username = unquote(re.findall('username=([^&]*)', data)[0])
        nickname = unquote(re.findall('nickname=([^&]*)', data)[0])
        password = unquote(re.findall('password=([^&]*)', data)[0])
        secretcode = unquote(re.findall('secretcode=([^&]*)', data)[0])
        result = yield model.register(
            self.application.mysql_db, username, nickname, password, secretcode
            )
        self.write(result)
        # if result is True:
        #     self.redirect("/login", permanent=True)
        # url = self.request.uri
        # self.render("register.html", url=url, username="登录", error=result)
