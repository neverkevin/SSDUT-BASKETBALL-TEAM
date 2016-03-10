# -*- coding: utf-8 -*-

from tornado import gen


@gen.coroutine
def GetContacts(mysql_db):
    contacts = mysql_db.query("select * from content")
    total_contacts = mysql_db.query("select count(*) from content")
    return contacts, str(total_contacts[0]["count(*)"])


@gen.coroutine
def AddContacts(mysql_db, name, grade, phonenum, place):
    sql = "insert into content (name, grade, phonenum, place) \
            values (%s, %s, %s, %s)"
    mysql_db.insert(sql, name, grade, phonenum, place)


@gen.coroutine
def login(mysql_db, username, password):
    usernameSQL = "select username from user where username=%s"
    is_username_exist = mysql_db.get(usernameSQL, username)
    if is_username_exist is not None:
        passwdSQL = "select password from user where username=%s"
        getpassword = mysql_db.get(passwdSQL, username)
        if getpassword["password"] == password:
            return '1'
        else:
            return "密码错误！"
    else:
        return "用户名不存在！"


@gen.coroutine
def get_nickname(mysql_db, username):
    getnicknameSQL = "select nickname from user where username=%s"
    nickname = mysql_db.get(getnicknameSQL, username)
    return nickname["nickname"]


@gen.coroutine
def register(mysql_db, username, nickname, password, secretcode):
    if secretcode != "secret":
        return "0"
    usernameSQL = "select username from user where username=%s"
    is_username_exist = mysql_db.get(usernameSQL, username)
    if is_username_exist:
        return "-1"
    sql = "INSERT INTO user (username, nickname, password) \
            VALUES (%s, %s, %s)"
    mysql_db.insert(sql, username, nickname, password)
    return "1"


@gen.coroutine
def check_username(mysql_db, username):
    sql = 'select username from user where username=%s'
    sql_username = mysql_db.get(sql, username)
    if sql_username == username:
        return '0'
    return '1'
