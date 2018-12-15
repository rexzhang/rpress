#!/usr/bin/env python
# coding=utf-8


from .base import ConfigBase

from flask_vises.deploy import DeployLevel


class Config(ConfigBase):
    # Deploy
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False

    DEPLOY_LEVEL = DeployLevel.release

    # Session/Cookie/Flask-Login
    SECRET_KEY = "THIS IS SECRET KEY, PLEASE CHANGE FOR PRODUCT ENVIRONMENT"

    # Sentry
    ConfigBase.SENTRY_CONFIG['ENVIRONMENT'] = 'release'
