#!/usr/bin/env python
# coding=utf-8


from flask_themes2 import render_theme_template

from rpress.runtimes.current_session import get_user_info, get_site_info


def render_template(template, content=None, **context):
    context['site'] = get_site_info()
    context['user'] = get_user_info()

    context['content'] = content

    return render_theme_template(context['site']['settings']['theme'], template, **context)
