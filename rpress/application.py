#!/usr/bin/env python
# coding=utf-8


from flask import Flask
from flask_themes2 import Themes
from flask_migrate import Migrate
from raven.contrib.flask import Sentry

from rpress.database import db
from rpress.permission import login_manager
from rpress.helpers.template.filter import configure_filter
from rpress.helpers.error_handler import configure_error_handler
from rpress.config import Config

from rpress.views import permission
from rpress.views import site_admin
from rpress.views import site_tools
from rpress.views import profiles_admin
from rpress.views import mulit_site_admin
from rpress.views import post as post_view

__all__ = ['create_app', 'create_app_for_cli']

DEFAULT_APP_NAME = 'rpress'

BLUE_PRINTS = (
    (post_view.post, ''),
    (permission.permission, ''),
    (site_admin.site_admin, '/rp/admin'),
    (site_tools.site_tools, '/rp/tools'),
    (profiles_admin.profiles_admin, '/rp/profiles'),
    (mulit_site_admin.mulit_site_admin, '/rp/mulitsite'),

    # add more blue print here
)


def create_app(app_name=DEFAULT_APP_NAME):
    app = Flask(app_name)
    app.config.from_object(Config())

    configure_sentry(app)

    configure_db(app)
    configure_theme(app)
    configure_permission(app)

    configure_filter(app)
    configure_error_handler(app)

    configure_blueprints(app)
    # configure_cache(app)

    return app


def create_app_for_cli(script_info):
    return create_app()


def configure_db(app):
    """"""
    db.init_app(app)
    Migrate(app, db)
    return


def configure_theme(app):
    """"""
    Themes(app, app_identifier='rpress')
    return


def configure_permission(app):
    """"""
    login_manager.setup_app(app)
    return


def configure_blueprints(app):
    for blue, url_prefix in BLUE_PRINTS:
        app.register_blueprint(blue, url_prefix=url_prefix)
    return


def configure_sentry(app):
    sentry_config = app.config.get('SENTRY_CONFIG', {})
    dsn = sentry_config.get('DSN', None)
    if dsn is not None:
        Sentry(app, dsn=dsn)

    return
