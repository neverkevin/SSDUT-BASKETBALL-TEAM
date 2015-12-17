#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import myTools
from datetime import datetime
from model import *

def login(email, password):
    if is_email_exist(email):
        user = UserCollection.find_one({'email': email})
        hashed_password = myTools.get_hashed_password(password, user['salt'])
        if hashed_password == user['password']:
            UserCollection.find_and_modify(
                query={'email': email},
                update={'$set': {'last_login': datetime.utcnow()}},
                upsert=False, full_response=True)
            return user
    return {}


def is_email_exist(email):
    if myTools.is_email(email):
        user = UserCollection.find_one({'email': email})
        if user:
            return True
        else:
            return False


def is_name_exist(name):
    user = UserCollection.find_one({'name': name})

    if user:
        return True
    else:
        return False


def insert_a_user(user):
    '''
    user = {
        'email': 'xxx@xx.xx',
        'name': 'xxxx',
        'password': 'xxxx',
        }
    '''
    password = user['password']
    salt = myTools.get_random_salt()
    hashed_password = myTools.get_hashed_password(password, salt)

    try:
        user['password'] = hashed_password
        user['salt'] = salt
        UserCollection.insert(user)
        return True
    except Exception, e:
        print traceback.print_exc()
        return False
