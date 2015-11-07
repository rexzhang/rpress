#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

import os
import logging

from flask import Flask
from flask.ext.themes2 import Themes
from flask.ext.migrate import Migrate

from rpress import db
from rpress import login_manager
from rpress.helpers.template.filter import configure_filter
from rpress.helpers.error_handler import configure_error_handler
from rpress.configs import get_config_obj

from rpress.views import permission
from rpress.views import site_admin
from rpress.views import profiles_admin
from rpress.views import mulit_site_admin
from rpress.views import post as post_view


__all__ = ['create_app']


DEFAULT_APP_NAME = 'rpress'

REGISTER_BLUE_PRINTS = (
    (post_view.post, ''),
    (permission.permission, ''),
    (site_admin.site_admin, '/rp/admin'),
    (profiles_admin.profiles_admin, '/rp/profiles'),
    (mulit_site_admin.mulit_site_admin, '/rp/mulitsite'),

    # add your blue print here
)

from rpress.helpers.template.common import render_template
def create_app(config_name=None,app_name=None):
    if app_name is None:
        app_name = DEFAULT_APP_NAME

    app = Flask(app_name)

    configure_app(app, config_name)
    configure_db(app)
    configure_theme(app)
    configure_permission(app)

    configure_filter(app)
    configure_error_handler(app)

    configure_blueprints(app)
    #configure_cache(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    return app


def configure_app(app, config_name):
    app.config.from_object(get_config_obj(config_name))

    #app.config.from_envvar('APP_CONFIG',silent=True)
    return


def configure_db(app):
    """"""
    db.init_app(app)
    migrate = Migrate(app, db)
    return


#----------------------------------------------------------------------
def configure_theme(app):
    """"""
    Themes(app, app_identifier='rpress')
    return


#----------------------------------------------------------------------
def configure_permission(app):
    """"""
    login_manager.setup_app(app)
    return


def configure_blueprints(app):
    for blue, url_prefix in REGISTER_BLUE_PRINTS:
        #app.register_blueprint(blue)
        app.register_blueprint(blue, url_prefix=url_prefix)
    return
