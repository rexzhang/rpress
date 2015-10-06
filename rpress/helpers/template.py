#!/usr/bin/env python
#coding=utf-8


#from flask import session
from flask.ext.themes2 import render_theme_template  #, get_themes_list



#----------------------------------------------------------------------
def render_template(template, **context):
    """"""
    #theme = session.get('theme', app.config['THEME_DEFAULT'])
    #return render_theme_template(theme, template, **context)
    return render_theme_template('rexzhangname', template, **context)
