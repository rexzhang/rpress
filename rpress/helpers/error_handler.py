#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from rpress.helpers.template.common import render_template


#----------------------------------------------------------------------
def page_not_found(e):
    """"""
    return render_template('404.html'), 404


#----------------------------------------------------------------------
def internal_server_error(e):
    """"""
    return render_template('500.html'), 500


#----------------------------------------------------------------------
def configure_error_handler(app):
    """"""
    app.register_error_handler(400, page_not_found)
    app.register_error_handler(500, internal_server_error)

    return