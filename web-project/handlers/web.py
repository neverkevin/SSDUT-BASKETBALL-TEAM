#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado
from baseHandler import BaseHandler
from operations.routes import route
from tornado import gen
import time
from models.model import *


@gen.coroutine
@route(r'/$', name='index')
class MainHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('index.html', url=url)


@route(r'/mingrentang$', name='mingrentang')
class MingrentangHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        contacts = GetContacts(self.application.mysql_db)
        self.render('mingrentang.html', contacts=contacts, url=url)


@route(r'/history/([0-9]+)$', name='history/([0-9]+)')
class HistoryHandler(BaseHandler):
    def get(self, history_id):
        self.write("You request the history_year: " + history_id)


@route(r'/add_contacts$', name='add_contacts')
class AddContactsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        url = self.request.uri
        self.render('add_contacts.html', url=url)

    def post(self):
        name = self.get_argument('name')
        grade = self.get_argument('grade')
        phonenum = self.get_argument('phonenum')
        place = self.get_argument('place')
        alert = AddContacts(self.application.mysql_db, name, grade, phonenum, place)
        self.redirect('/add_contacts', permanent=True)


@route(r'/login$', name='login')
class LoginHandler(BaseHandler):
    def get(self):
        url = self.request.uri
        self.render('login.html', url=url)

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        tag = login(self.application.mysql_db, username, password)
        if tag:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/add_contacts", permanent=True)
        else:
            self.redirect("/login", permanent=True)


@route(r'/test_model$', name='test_model')
class TestModelHandler(BaseHandler):
    def get(self):
        res = 'test_model title: <br>'
        for test in TestModel.objects:
            res += '<br>' + test.title
        self.write(res)

    def post(self):
        title = self.get_argument('title')
        text = self.get_argument('title')
        tmp_model = TestModel(title, text)
        tmp_model.save()
