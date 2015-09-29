#!/usr/bin/env python
#coding=utf-8


import hashlib

import flask.ext.login

from rpress.models import User


login_manager = flask.ext.login.LoginManager()


########################################################################
class LoginUser(flask.ext.login.UserMixin):
    """user object for login. make User.id to user_id"""
    id = None
    #----------------------------------------------------------------------
    def get_id(self):
        """"""
        if self.id is None:
            raise NotImplementedError('`id` == None')

        return self.id


@login_manager.user_loader
def load_user(user_id):
    """TODO:会导致一次数据查询，需要迁移到内存类容器中处理"""
    print 'user_id:', user_id
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return None

    loginUser = LoginUser()
    loginUser.id = user.id

    return loginUser


#----------------------------------------------------------------------
def login_user(username, password):
    """
    check a pair of username and password , and more...

    :rtype: (True or False)
    """
    user = User.query.filter_by(name=username).first()
    if user is None:
        return False

    if user.password != hashlib.sha256(password).hexdigest():
        return False

    loginUser = LoginUser()
    loginUser.id = user.id

    flask.ext.login.login_user(loginUser)

    return True


#----------------------------------------------------------------------
def logout_user():
    """"""
    flask.ext.login.logout_user()
    return
