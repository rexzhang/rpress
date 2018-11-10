#!/usr/bin/env python
# coding=utf-8


from rpress.constants import SITE_SETTINGS_KEY_LIST
from rpress.models import SiteSetting


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
