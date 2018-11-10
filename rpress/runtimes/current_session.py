#!/usr/bin/env python
# coding=utf-8


from flask_login import current_user

from rpress.helpers.mulit_site import get_current_request_site
from rpress.helpers.site import get_site_settings


def get_user_info():
    """current session user info"""
    if not current_user.is_active:
        return None

    return {
        'id': current_user.id,
        'name': current_user.name,
    }


def get_site_info():
    """current session site info"""
    site = get_current_request_site()  # TODO: redis cache site info
    if site is None:
        return None

    return {
        'id': site.id,
        'domain': site.domain,
        'settings': get_site_settings(site),
    }
