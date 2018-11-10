#!/usr/bin/env python
# coding=utf-8


from pprint import pprint

from flask import g

from rpress.runtimes.current_session import get_current_request_site


def current_request_site(func):
    """"""
    def _set_current_request_site(*args, **kwargs):
        site = get_current_request_site()
        pprint(args)

        g.current_request_site = site

        return func(*args, **kwargs)

    return _set_current_request_site
