#!/usr/bin/env python
# coding=utf-8


import logging

import flask_login

from rpress.models import User
from rpress.runtimes.password import check_password_hash

login_manager = flask_login.LoginManager()
logger = logging.Logger(__name__)


class LoggedUser(flask_login.UserMixin):
    """user object for login. make User.id to user_id"""
    id = None
    name = None

    def get_id(self):
        if self.id is None:
            raise NotImplementedError('`id` == None')

        return self.id


def _init_logged_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return None

    logged_user = LoggedUser()
    logged_user.id = user.id
    logged_user.name = user.name

    return logged_user


@login_manager.user_loader
def user_loader(user_id):
    return _init_logged_user(user_id=user_id)


@login_manager.request_loader
def request_loader(load_request):
    user_id = load_request.form.get('user_id')
    if not user_id:
        return None

    return _init_logged_user(user_id=user_id.id)


def user_login(username, password):
    """
    check a pair of username and password , and more...

    :rtype: (True or False)
    """
    user = User.query.filter_by(name=username).first()
    if user is None:
        logger.warning('can not match user name')
        return False

    if not check_password_hash(password, user.password):
        logger.warning('can not match password')
        return False

    logged_user = _init_logged_user(user_id=user.id)
    flask_login.login_user(logged_user)

    logger.info('login finished')
    return True


def user_logout():
    flask_login.logout_user()
    return
