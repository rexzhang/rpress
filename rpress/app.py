#!/usr/bin/env python
#coding=utf-8


import os
import logging
from flask import Flask

from rpress import configs

#from rpress.views import test_view as test
from rpress import views as test
# add some other view

__all__ = ['create_app']


DEFAULT_APP_NAME = 'rpress'

REGISTER_BLUE_PRINTS = (
    (test.instance, ''),
    # add your blue print here
)


def create_app(config=None,app_name=None):

    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)

    configure_app(app,config)
    #configure_db(app)
    configure_blueprints(app)
    #configure_cache(app)
    return app


def configure_app(app,config):
    app.config.from_object(configs.ConfigDev())

    if config is not None:
        app.config.from_object(config)

    app.config.from_envvar('APP_CONFIG',silent=True)
    return


def configure_db(app):
    pass


def configure_blueprints(app):
    for blue,url_prefix in REGISTER_BLUE_PRINTS:
        #app.register_blueprint(blue)
        app.register_blueprint(blue,url_prefix=url_prefix)
    return
