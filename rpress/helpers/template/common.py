#!/usr/bin/env python
#coding=utf-8


from flask import request
from flask.ext.themes2 import render_theme_template  #, get_themes_list
from flask.ext.login import current_user

from rpress.models import Site, SiteSetting
from rpress.helpers.mulit_site import get_current_request_site


#----------------------------------------------------------------------
def _site_settings():
    """"""
    site = get_current_request_site()
    if site is None:
        site = Site.query.filter_by(id=1).first()

    site_title = SiteSetting.query.filter_by(site=site, key='title').first()
    site_desc = SiteSetting.query.filter_by(site=site, key='desc').first()
    site_disqus = SiteSetting.query.filter_by(site=site, key='disqus').first()

    site_info = {
        'title': site_title.value,
        'desc': site_desc.value,
        'disqus': site_disqus,
    }
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

    #theme = session.get('theme', app.config['THEME_DEFAULT'])
    #return render_theme_template(theme, template, **context)
    return render_theme_template('rexzhangname', template, **context)
