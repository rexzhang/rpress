#!/usr/bin/env python
#coding=utf-8


"""
for Flask-Script prompt
"""

from __future__ import print_function, unicode_literals, absolute_import

from flask_script import Manager, prompt_bool, prompt

from rpress import db
from rpress.models import User


#----------------------------------------------------------------------
def ask_user_name():
    """ask user name"""
    user_name = prompt('user name')
    return user_name


#----------------------------------------------------------------------
def create_new_user_with_default_password(user_name=None):
    """ask did you create it

    ret: None #skip create
    """
    is_new_user = False

    #input user name
    if user_name is None:
        user_name = prompt('user name')

    #check user name
    user = User.query.filter_by(name=user_name).first()
    if user is not None:
        print('duplicate user name!')
        return None

    #confirm for human
    if not prompt_bool('[{}] is a new user name, did you create it?'.format(user_name), default=True):
        return None

    #create it
    user = User(name=user_name, password='password')

    return user
