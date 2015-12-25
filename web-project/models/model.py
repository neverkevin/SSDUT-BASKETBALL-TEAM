#!/usr/bin/env python
# encoding=utf-8

import torndb


def GetContacts(mysql_db):
    contacts = mysql_db.query('select * from content')
    return contacts


def AddContacts(mysql_db, name, grade, phonenum, place):
    sql = 'insert into content (name, grade, phonenum, place) values (%s, %s, %s, %s)'
    mysql_db.insert(sql, name, grade, phonenum, place)


def login(mysql_db, username, password):
    usernameSQL= 'select username from user where username=%s'
    is_username_exist = mysql_db.get(usernameSQL, username)
    if is_username_exist is not None:
        passwdSQL = 'select password from user where username=%s'
        getpassword = mysql_db.get(passwdSQL, username)
        if getpassword['password'] == password:
            return True
        else:
            return False
    else:
        return False
