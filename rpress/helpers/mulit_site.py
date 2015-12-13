#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from flask import g, request

from rpress.models import Site


#----------------------------------------------------------------------
def get_current_request_site_domain():
    """"""
    return request.environ['HTTP_HOST'].split(':')[0]


#----------------------------------------------------------------------
def get_current_request_site():
    """return site object for current request"""
    domain = get_current_request_site_domain()

    site = Site.query.filter_by(domain=domain).first()
    if site is None:
        if domain == 'localhost' or domain == '127.0.0.1':
            site = Site.query.filter_by(id=1).first()
        else:
            return None

    return site


from pprint import pprint
#----------------------------------------------------------------------
def current_request_site(func):
    """"""
    def _set_current_request_site(*args, **kwargs):
        site = get_current_request_site()
        pprint(args)

        g.current_request_site = site

        return func(*args, **kwargs)

    return _set_current_request_site
