# -*- coding: utf-8 -*-

import hashlib
import sys
from tornado import gen

reload(sys)
sys.setdefaultencoding('utf8')


def md5(data):
    md5 = hashlib.md5()
    data = data + 'secret'
    md5.update(data)
    return md5.hexdigest()


@gen.coroutine
def get_contacts(db):
    contacts = db.query("select * from contacts")
    total_contacts = db.query("select count(*) from contacts")
    return contacts, str(total_contacts[0]["count(*)"])


@gen.coroutine
def add_contacts(db, contacts):
    sql = "insert into contacts (name, grade, phonenum, place) \
            values (%s, %s, %s, %s)"
    db.insert(
        sql, contacts.name, contacts.grade, contacts.phonenum, contacts.place
        )


@gen.coroutine
def login(db, user):
    usernameSQL = "select username from user where username=%s"
    is_username_exist = db.get(usernameSQL, user.username)
    if is_username_exist is not None:
        passwdSQL = "select password from user where username=%s"
        password = md5(user.password)
        getpassword = db.get(passwdSQL, user.username)
        if getpassword["password"] == password:
            return '1'
        return "密码错误！"
    return "用户名不存在！"


@gen.coroutine
def get_nickname(db, username):
    getnicknameSQL = "select nickname from user where username=%s"
    nickname = db.get(getnicknameSQL, username)
    return nickname["nickname"]


@gen.coroutine
def register(db, user, secretcode):
    if secretcode != "secret":
        return "0"
    usernameSQL = "select username from user where username=%s"
    is_username_exist = db.get(usernameSQL, user.username)
    if is_username_exist:
        return "-1"
    password = md5(user.password)
    sql = "INSERT INTO user (username, nickname, password) \
            VALUES (%s, %s, %s)"
    db.insert(sql, user.username, user.nickname, password)
    return "1"


@gen.coroutine
def check_username(db, username):
    sql = 'select username from user where username=%s'
    sql_username = db.get(sql, username)
    if sql_username == username:
        return '0'
    return '1'


@gen.coroutine
def fix_user(db, nickname, user):
    sql = 'update user set grade=%s, phonenum=%s, place=%s where nickname=%s'
    result = db.update(sql, user.grade, user.phonenum, user.place, nickname)
    return str(result)


@gen.coroutine
def get_user(db, nickname):
    sql = 'select * from user where nickname=%s'
    result = db.get(sql, nickname)
    return result
