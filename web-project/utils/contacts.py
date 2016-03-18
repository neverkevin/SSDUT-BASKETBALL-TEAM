#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base_object import BaseObject


class Contacts(BaseObject):

    table = 'contacts'
    keyMapping = (
        'cid', 'name', 'grade',
        'phonenum', 'place'
        )

    def __init__(self, data=None):
        self.cid = ''
        self.name = ''
        self.grade = ''
        self.phonenum = ''
        self.place = ''

        BaseObject.__init__(self, data)
