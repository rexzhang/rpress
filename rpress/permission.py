#!/usr/bin/env python
#coding=utf-8


import hashlib

import flask_login

from rpress.models import User


login_manager = flask_login.LoginManager()


########################################################################
class LoggedUser(flask_login.UserMixin):
    """user object for login. make User.id to user_id"""
    id = None

    #----------------------------------------------------------------------
    def get_id(self):
        """"""
        if self.id is None:
            raise NotImplementedError('`id` == None')

        return self.id


@login_manager.user_loader
def user_loader(user_id):
    """TODO:会导致一次数据查询，需要迁移到内存类容器中处理"""
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return None

    logged_user = LoggedUser()
    logged_user.id = user.id

    return logged_user


#----------------------------------------------------------------------
def user_login(username, password):
    """
    check a pair of username and password , and more...

    :rtype: (True or False)
    """
    user = User.query.filter_by(name=username).first()
    if user is None:
        return False

    if user.password != hashlib.sha256(password).hexdigest():
        return False

    logged_user = LoggedUser()
    logged_user.id = user.id

    flask_login.login_user(logged_user)

    return True


#----------------------------------------------------------------------
def user_logout():
    """"""
    flask_login.logout_user()
    return
