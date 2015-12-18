#!/usr/bin/env python
# encoding=utf-8

from mongoengine import *
import torndb
import MySQLdb
import pymongo

class TestModel(Document):

    """Test Mongoengine"""

    title = StringField(required=True)
    text = StringField()


def GetContacts(mysql_db):
    contacts = mysql_db.query('select * from content')
    return contacts


def AddContacts(mysql_db, name, grade, phonenum, place):
    sql = 'insert into content (name, grade, phonenum, place) values (%s, %s, %s, %s)'
    mysql_db.insert(sql, name, grade, phonenum, place)
