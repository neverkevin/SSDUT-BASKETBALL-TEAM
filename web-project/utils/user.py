#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_object import BaseObject


class User(BaseObject):

    table = 'user'
    keyMapping = (
        'uid', 'username', 'password', 'nickname',
        'grade', 'phonenum', 'place'
        )

    def __init__(self, data=None):
        self.uid = ''
        self.username = ''
        self.password = ''
        self.nickname = ''
        self.grade = ''
        self.phonenum = ''
        self.place = ''

        BaseObject.__init__(self, data)
