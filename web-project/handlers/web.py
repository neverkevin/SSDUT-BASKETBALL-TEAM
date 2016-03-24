# /usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
from urllib import quote
from tornado import gen
from baseHandler import BaseHandler
from operations.routes import route
from utils.contacts import Contacts
from utils.user import User
from models import model
from models import music


@route(r'/$', name='home')
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
        contacts, total_contacts = yield model.get_contacts(
            self.db
            )
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
        data = self.request.arguments
        contacts = Contacts(data)
        yield model.add_contacts(
            self.db, contacts
            )
        self.redirect('/HallofFame', permanent=True)


@route(r'/user/\S+', name='user')
class UserHandler(BaseHandler):
    @gen.coroutine
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        username = tornado.escape.xhtml_escape(self.current_user)
        if url != '/user/{}'.format(quote(username)):
            raise tornado.web.HTTPError(403)
        data = yield model.get_user(
            self.application.db, username
            )
        user = User(data)
        self.render('user.html', url=url, username=username, user=user)

    @gen.coroutine
    def post(self):
        nickname = tornado.escape.xhtml_escape(self.current_user)
        data = self.request.arguments
        user = User(data)
        result = yield model.fix_user(
            self.db, nickname, user
            )
        self.write(result)


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
        data = self.request.arguments
        user = User(data)
        result = yield model.login(
            self.db, user
            )
        if result == '1':
            nickname = yield model.get_nickname(
                self.db, user.username
                )
            self.set_secure_cookie("user", nickname)
        self.write(result)


@route(r'/check_username', name='checkout_username')
class CheckUsernameHandler(BaseHandler):
    @gen.coroutine
    def post(self):
        username = self.get_argument('username')
        result = yield model.check_username(
            self.db, username
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
        data = self.request.arguments
        secretcode = self.get_argument('secretcode')
        user = User(data)
        result = yield model.register(
            self.db, user, secretcode
            )
        self.write(result)
