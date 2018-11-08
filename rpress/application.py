#!/usr/bin/env python
# coding=utf-8


from flask import Flask
from flask_themes2 import Themes
from flask_vises.database import configure_db
from raven.contrib.flask import Sentry

from rpress.constants import APP_NAME
from rpress.database import db
from rpress.runtimes.auth import login_manager
from rpress.helpers.template.filter import configure_filter
from rpress.helpers.error_handler import configure_error_handler
from rpress.config import Config
from rpress import views

__all__ = ['create_app', 'create_app_for_cli', 'create_app_for_testing']

BLUE_PRINTS = (
    (views.post.post_page, ''),
    (views.auth.auth, ''),

    (views.rpadmin.dashboard.app, '/rp/admin/dashboard'),
    (views.rpadmin.profile.app, '/rp/admin/profile'),
    (views.rpadmin.post.app, '/rp/admin/post'),
    (views.rpadmin.setting.app, '/rp/admin/settings'),
    (views.rpadmin.site.app, '/rp/admin/site'),

    (views.site_admin.site_admin, '/rp/admin'),
    (views.site_tools.site_tools, '/rp/tools'),

    # add more blue print here
)


def create_app(testing=False):
    app = Flask(APP_NAME)
    app.config.from_object(Config())

    if testing:
        from flask_vises.testing import configure_testing

        configure_testing(app)

    configure_sentry(app)

    configure_db(app, db)
    configure_theme(app)
    configure_permission(app)

    configure_filter(app)
    configure_error_handler(app)

    configure_blueprints(app)

    return app


def create_app_for_cli(script_info):
    return create_app()


def create_app_for_testing():
    return create_app(testing=True)


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
