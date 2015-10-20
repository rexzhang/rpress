#!/usr/bin/env python
#coding=utf-8


#from flask import session
from flask.ext.themes2 import render_theme_template  #, get_themes_list
from flask.ext.login import current_user

from rpress.models import Site


#----------------------------------------------------------------------
def _site_info():
    """"""
    site = Site.query.filter_by(id=1).first()

    site_info = {
        'name': site.name,
        'title': site.title,
        'desc': site.desc,
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
