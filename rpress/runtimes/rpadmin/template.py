#!/usr/bin/env python
# coding=utf-8


from functools import wraps

from flask import g
# from flask import render_template as render_flask_template  # TODO: can not work!
from flask_themes2 import render_theme_template

from rpress.runtimes.current_session import get_current_user_info, get_current_site_info


def render_template(template, content=None, **context):
    context['site'] = get_current_site_info()
    context['user'] = get_current_user_info()

    context['content'] = content

    return render_theme_template('default', template, **context)


def set_navbar(level1, level2=None):
    # 'key' = None
    # g.key => None, g.key.k2 BOOM!
    g.navbar_lv1 = level1
    g.navbar_lv2 = level2
    return


def navbar(level1, level2=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            set_navbar(level1=level1, level2=level2)

            return f(*args, **kwargs)

        return wrapper

    return decorator
