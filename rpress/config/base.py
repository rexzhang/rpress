#!/usr/bin/env python
# coding=utf-8


from datetime import timedelta

from flask_vises.deploy import DeployLevel


class ConfigBase(object):
    # 项目根路径
    # ROOT_PATH = getcwd()

    # Deploy
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

    DEPLOY_LEVEL = DeployLevel.develop

    # Continuous Integration
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = 'postgresql://rex@localhost/rpress_develop?client_encoding=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session/Cookie/Flask-Login
    SECRET_KEY = "this is secret key, please change for product environment"

    REMEMBER_COOKIE_DOMAIN = 'rpress.sgfans.org'
    REMEMBER_COOKIE_DURATION = timedelta(hours=8)

    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # Theme
    THEME_DEFAULT = 'rexzhangname'

    # Sentry
    SENTRY_CONFIG = {
        'DSN': None,
        'ENVIRONMENT': 'rPress-develop',
    }
