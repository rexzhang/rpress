#!/usr/bin/env python
#coding=utf-8


import os
import logging

from flask import Flask
from flask.ext.themes2 import Themes

from rpress.configs import ConfigDev
from rpress.database import db

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

    configure_app(app, config)
    configure_db(app)
    configure_theme(app)
    configure_blueprints(app)
    #configure_cache(app)
    return app
    #return


def configure_app(app, config):
    if config is not None:
        app.config.from_object(config)
    else:
        app.config.from_object(ConfigDev)

    #app.config.from_envvar('APP_CONFIG',silent=True)
    return


def configure_db(app):
    """"""
    db.init_app(app)
    return


#----------------------------------------------------------------------
def configure_theme(app):
    """"""
    Themes(app, app_identifier='rpress')
    return


def configure_blueprints(app):
    for blue,url_prefix in REGISTER_BLUE_PRINTS:
        #app.register_blueprint(blue)
        app.register_blueprint(blue,url_prefix=url_prefix)
    return
