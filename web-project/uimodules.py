#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado

class Navbar(tornado.web.UIModule):
    def render(self, brand, navs, login):
        return self.render_string("header.html", brand=brand, navs=navs, login=login)


class NavbarHeader(Navbar):
    def render(self, url, username):
        brand = {}
        brand['name'] = 'SSDUT 篮球队'
        brand['href'] = '/'
        navs = [{ }]
        navs[0]['name'] = '名人堂'
        navs[0]['href'] = '/mingrentang'
        login = {}
        login['name'] = username
        login['href'] = '/login'
        if url == '/':
            brand['active'] = True
        elif url == '/mingrentang':
            navs[0]['active'] = True
        elif url == '/login':
            login['active'] = True
        else:
            pass
        return Navbar.render(self, brand, navs, login)


class Grade(tornado.web.UIModule):
    def render(self, grades):
        return self.render_string("right_navigation.html", grades=grades)


class GradeRight(Grade):
    def render(self, url):
        grades = []
        for i in xrange(len(xrange(2006, 2016))):
            grades.append({})

        for i, n in enumerate(xrange(2006, 2016)):
            grades[i]['name'] = n
            grades[i]['url'] = '/history/%s' % n
            if url == '/history/%s' % n:
                grades[i]['active'] = True
        return Grade.render(self, grades)
