#!/usr/bin/env python
# coding=utf-8


from flask_themes2 import render_theme_template
from flask_login import current_user

from rpress.helpers.site import get_current_request_site_info


def _user_info():
    """"""
    if not current_user.is_active:
        return None

    user_info = {
        'id': current_user.id,
        'name': current_user.name,
    }

    return user_info


def render_template(template, **context):
    """"""
    context['site'] = get_current_request_site_info()
    context['user'] = _user_info()

    return render_theme_template(context['site']['settings']['theme'], template, **context)
