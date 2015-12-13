#!/usr/bin/env python
#coding=utf-8


from flask import request
from flask.ext.themes2 import render_theme_template  #, get_themes_list
from flask.ext.login import current_user

from rpress.constants import SITE_SETTINGS_KEY_LIST
from rpress.models import Site, SiteSetting
from rpress.helpers.mulit_site import get_current_request_site


#----------------------------------------------------------------------
def _site_settings():
    """"""
    site = get_current_request_site()
    if site is None:
        site = Site.query.filter_by(id=1).first()

    site_info = {
        'domain': site.domain,
    }

    for key in SITE_SETTINGS_KEY_LIST:
        setting = SiteSetting.query.filter_by(site=site, key=key).first()
        if setting is None or len(setting.value) == 0:
            site_info[key] = None
        else:
            site_info[key] = setting.value

    if site_info['theme'] is None:
        site_info['theme'] = 'default'

    return site_info


#----------------------------------------------------------------------
def _user_info():
    """"""
    if not current_user.is_active:
        return None

    user_info = {
        'id': current_user.id,
    }

    return user_info


#----------------------------------------------------------------------
def render_template(template, **context):
    """"""
    context['site'] = _site_settings()
    context['user'] = _user_info()

    return render_theme_template(context['site']['theme'], template, **context)
