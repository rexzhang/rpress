#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from flask import g, request

from rpress.models import Site


#----------------------------------------------------------------------
def get_current_request_site():
    """return site object for current request"""
##    from pprint import pprint
##    pprint(request.environ['HTTP_HOST'])

    site = Site.query.filter_by(domain=request.environ['HTTP_HOST'].split(':')[0]).first()
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
