#!/usr/bin/env python
# coding=utf-8


from flask_themes2 import render_theme_template

from rpress.runtimes.current_session import get_current_user_info, get_current_site_info


def render_template(template, content=None, **context):
    context['site'] = get_current_site_info()
    context['user'] = get_current_user_info()

    context['content'] = content

    return render_theme_template(context['site']['settings']['theme'], template, **context)


def filter_datetime_short(value):
    if value is None:
        return str(None)

    return value.strftime(format="%Y-%m-%d")


def filter_datetime_long(value):
    if value is None:
        return str(None)

    return value.strftime(format="%Y-%m-%d %H:%M:%S")


def configure_filter(app):
    @app.template_filter()
    def datetime_short(value):
        return filter_datetime_short(value)

    @app.template_filter()
    def datetime_long(value):
        return filter_datetime_long(value)
