#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado

class Navbar(tornado.web.UIModule):
    def render(self, brand, navs):
        return self.render_string("header.html", brand=brand, navs=navs)

class NavbarSSDUT(Navbar):
    def render(self, url):
        brand = {}
        brand['href'] = '/'
        brand['name'] = 'SSDUT 篮球队'
        navs = [{ }, { }, { }]
        navs[0]['name'] = '名人堂'
        navs[0]['href'] = '/mingrentang'
        navs[1]['name'] = '添加联系人'
        navs[1]['href'] = '/add_contacts'
        navs[2]['name'] = '登录'
        navs[2]['href'] = '/login'
        if url == '/':
            brand['active'] = True
        elif url == '/mingrentang':
            navs[0]['active'] = True
        elif url == '/add_contacts':
            navs[1]['active'] = True
        elif url == '/login':
            navs[2]['active'] = True
        return Navbar.render(self, brand, navs)
