#!/usr/bin/env python
#coding=utf-8


#from flask import session
from flask.ext.themes2 import render_theme_template  #, get_themes_list
from flask.ext.login import current_user

from rpress.models import Site, SiteSetting


#----------------------------------------------------------------------
def _site_info():
    """"""
    site = Site.query.filter_by(id=1).first()
    site_title = SiteSetting.query.filter_by(site=site, key='title').first()
    site_desc = SiteSetting.query.filter_by(site=site, key='desc').first()

    site_info = {
        'name': site.name,
        'title': site_title.value,
        'desc': site_desc.value,
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
    context['site'] = _site_info()
    context['user'] = _user_info()

    #theme = session.get('theme', app.config['THEME_DEFAULT'])
    #return render_theme_template(theme, template, **context)
    return render_theme_template('rexzhangname', template, **context)
