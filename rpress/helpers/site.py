#!/usr/bin/env python
#coding=utf-8


from __future__ import print_function, unicode_literals, absolute_import

from rpress.constants import SITE_SETTINGS_KEY_LIST
from rpress.models import Site, SiteSetting
from rpress.helpers.mulit_site import get_current_request_site


#----------------------------------------------------------------------
def get_current_request_site_info():
    """"""
    site = get_current_request_site()
    if site is None:
        return None

    site_info = {
        'id': site.id,
        'domain': site.domain,
        'settings': get_site_settings(site),
    }

    return site_info


#----------------------------------------------------------------------
def get_site_settings(site):
    """
    site: Site Model object
    """
    site_settings = {}

    for key in SITE_SETTINGS_KEY_LIST:
        setting = SiteSetting.query.filter_by(site=site, key=key).first()
        if setting is None or len(setting.value) == 0:
            site_settings[key] = None
        else:
            site_settings[key] = setting.value

    if site_settings['theme'] is None:
        site_settings['theme'] = 'default'

    return site_settings


#----------------------------------------------------------------------
def get_current_request_site_settings():
    """"""
    site = get_current_request_site()
    if site is None:
        return None

    return get_site_settings(site)
