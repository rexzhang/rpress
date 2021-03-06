#!/usr/bin/env python
# coding=utf-8


from datetime import timedelta

from flask_vises.config import ConfigAbstract
from flask_vises.deploy import DeployLevel


class ConfigBase(ConfigAbstract):
    # Deploy
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

    DEPLOY_LEVEL = DeployLevel.develop

    # Continuous Integration
    TESTING = False

    # Database
    ConfigAbstract.SQLALCHEMY_DATABASE['ENGINE'] = 'postgresql'
    ConfigAbstract.SQLALCHEMY_DATABASE['HOST'] = 'localhost'
    ConfigAbstract.SQLALCHEMY_DATABASE['PORT'] = '5432'
    ConfigAbstract.SQLALCHEMY_DATABASE['NAME'] = 'rpress'
    ConfigAbstract.SQLALCHEMY_DATABASE['USER'] = 'rpress'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session/Cookie/Flask-Login
    SECRET_KEY = "this is secret key, please change for product environment"

    REMEMBER_COOKIE_DOMAIN = 'rpress.sgfans.org'
    REMEMBER_COOKIE_DURATION = timedelta(hours=8)

    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    # Theme
    THEME_DEFAULT = 'default'

    # Sentry
    SENTRY_CONFIG = {
        'DSN': None,
        'ENVIRONMENT': 'develop',
    }
